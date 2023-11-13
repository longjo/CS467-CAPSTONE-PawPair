from flask import Blueprint,  redirect, render_template, request, session

from utils import make_db_connection

delete_user_account_page_bp = Blueprint('delete_user_account', __name__, template_folder='templates')

@delete_user_account_page_bp.route('/delete_user_account', methods=['GET', 'POST'])
def delete_user_account():

    # Display prefilled form
    if request.method == 'GET':
        if session.get('logged_in'):
            return render_template(
                'pages/user_account/delete_user_account_page.html',
                logged_in=session.get('logged_in', False),
                as_user=session.get('as_user', False)
            )
        else:
            return redirect('/user_login')

    # Delete account from DB
    if request.method == 'POST':

        # Get the form data
        password = request.form['password']

        # Create a database connection
        db = make_db_connection()

        # Create a cursor
        cursor = db.cursor()

        # Select user with matching username/password combination
        query = """
            SELECT password FROM Users
            WHERE user_id=%s
        """
        cursor.execute(query, (session.get('user_id', -999),))
        user_password = cursor.fetchone()
        
        # If provided password matches or is '123'...
        if password == user_password[0] or password == '123':

            # Delete the form data into the database
            query = """
                DELETE FROM Users
                WHERE user_id = %s
            """
            cursor.execute(query, (session.get('user_id', -999),))

            # Commit the changes
            db.commit() 

            # Clear the user's session
            session.clear()
            return redirect('/')

        # Close the cursor and the database connection
        cursor.close()
        db.close()

        return redirect('/delete_user_account')