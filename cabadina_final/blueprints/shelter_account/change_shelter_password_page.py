from flask import Blueprint,  redirect, render_template, request, session

from utils import make_db_connection

change_shelter_password_page_bp = Blueprint('change_shelter_password', __name__, template_folder='templates')

@change_shelter_password_page_bp.route('/change_shelter_password', methods=['GET', 'POST'])
def change_shelter_password():

    # Display prefilled form
    if request.method == 'GET':
        return render_template(
            'pages/shelter_account/change_shelter_password_page.html',
            logged_in=session.get('logged_in', False),
            as_user=session.get('as_user', False)
        )

    # Write to DB
    if request.method == 'POST':

        # Get the form data
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        new_password_check = request.form['new_password_check']

        if new_password != new_password_check:
            return render_template(
                'pages/shelter_account/change_shelter_password_page.html',
                logged_in=session.get('logged_in', False),
                as_user=session.get('as_user', False),
                error=True
            )

        # Create a database connection
        db = make_db_connection()

        # Create a cursor
        cursor = db.cursor()

        # Select password of current shelter
        query = """
            SELECT password FROM Shelters
            WHERE shelter_id=%s
        """
        cursor.execute(query, (session.get('shelter_id', -999),))
        shelter_password = cursor.fetchone()

        # If provided password doesn't match
        if current_password != shelter_password[0]:

            # Close the cursor and the database connection
            cursor.close()
            db.close()

            # Go back and indicate the error    
            return render_template(
                'pages/shelter_account/change_shelter_password_page.html',
                logged_in=session.get('logged_in', False),
                as_user=session.get('as_user', False),
                error=True
            )

        else:
            # Insert the new password into the database
            query = """
                UPDATE Shelters
                SET password = %s
                WHERE shelter_id = %s
            """
            cursor.execute(query, (new_password, session.get('shelter_id', -999)))

            # Commit the changes
            db.commit()
            
            # Close the cursor and the database connection
            cursor.close()
            db.close()

            return redirect('/shelter_account')