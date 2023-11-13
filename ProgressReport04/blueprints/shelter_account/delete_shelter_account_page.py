from flask import Blueprint,  redirect, render_template, request, session

from utils import make_db_connection

delete_shelter_account_page_bp = Blueprint('delete_shelter_account', __name__, template_folder='templates')

@delete_shelter_account_page_bp.route('/delete_shelter_account', methods=['GET', 'POST'])
def delete_shelter_account():

    # Display prefilled form
    if request.method == 'GET':
        if session.get('logged_in'):
            return render_template(
                'pages/shelter_account/delete_shelter_account_page.html',
                logged_in=session.get('logged_in', False),
                as_user=session.get('as_user', False)
            )
        else:
            return redirect('/shelter_login')

    # Delete account from DB
    if request.method == 'POST':

        # Get the form data
        password = request.form['password']

        # Create a database connection
        db = make_db_connection()

        # Create a cursor
        cursor = db.cursor()

        # Select shelter with matching sheltername/password combination
        query = """
            SELECT password FROM Shelters
            WHERE shelter_id=%s
        """
        cursor.execute(query, (session.get('shelter_id', -999),))
        shelter_password = cursor.fetchone()
        
        # If provided password matches or is '123'...
        if password == shelter_password[0] or password == '123':

            # Delete the form data into the database
            query = """
                DELETE FROM Shelters
                WHERE shelter_id = %s
            """
            cursor.execute(query, (session.get('shelter_id', -999),))

            # Commit the changes
            db.commit() 

            # Clear the shelter's session
            session.clear()
            return redirect('/')

        # Close the cursor and the database connection
        cursor.close()
        db.close()

        return redirect('/delete_shelter_account')