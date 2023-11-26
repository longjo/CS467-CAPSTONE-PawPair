from flask import Blueprint,  redirect, render_template, request, session

from utils import make_db_connection

change_user_password_page_bp = Blueprint('change_user_password', __name__, template_folder='templates')

@change_user_password_page_bp.route('/change_user_password', methods=['GET', 'POST'])
def change_user_password():

    # Display prefilled form
    if request.method == 'GET':
        return render_template(
            'pages/user_account/change_user_password_page.html',
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
                'pages/user_account/change_user_password_page.html',
                logged_in=session.get('logged_in', False),
                as_user=session.get('as_user', False),
                error=True
            )

        # Create a database connection
        db = make_db_connection()

        # Create a cursor
        cursor = db.cursor()

        # Select password of current user
        query = """
            SELECT password FROM Users
            WHERE user_id=%s
        """
        cursor.execute(query, (session.get('user_id', -999),))
        user_password = cursor.fetchone()

        # If provided password doesn't match
        if current_password != user_password[0]:

            # Close the cursor and the database connection
            cursor.close()
            db.close()

            # Go back and indicate the error    
            return render_template(
                'pages/user_account/change_user_password_page.html',
                logged_in=session.get('logged_in', False),
                as_user=session.get('as_user', False),
                error=True
            )

        else:
            # Insert the new password into the database
            query = """
                UPDATE Users
                SET password = %s
                WHERE user_id = %s
            """
            cursor.execute(query, (new_password, session.get('user_id', -999)))

            # Commit the changes
            db.commit()
            
            # Close the cursor and the database connection
            cursor.close()
            db.close()

            return redirect('/user_account')