from flask import Blueprint,  redirect, render_template, request, session

from utils import make_db_connection

user_login_page_bp = Blueprint('user_login', __name__, template_folder='templates')

@user_login_page_bp.route('/user_login', methods=['GET', 'POST'])
def user_login():

    # Redirect already logged in users
    logged_in=session.get('logged_in', False)
    as_user=session.get('as_user', False)
    print(logged_in, as_user)

    if logged_in:
        if as_user:
            return redirect('/user_account')
        else:
            return redirect('/shelter_account')

    # GET: Display user login page
    if request.method == 'GET':
        return render_template(
            'pages/auth/user_login_page.html',
            logged_in=logged_in,
            as_user=as_user
        )
    
    # POST: Attempt user login
    if request.method == 'POST':

        # Get the form data
        email = request.form['email']
        password = request.form['password']

        # Create a db connection and cursor
        db = make_db_connection()
        cursor = db.cursor()

        # Verify login credentials match stored data
        query = """
            SELECT * FROM Users
            WHERE email=%s AND password=%s
        """
        cursor.execute(query, (email, password))
        user = cursor.fetchone()

        # Close the connection
        cursor.close()
        db.close()

        # Credentials match: log in then send to account page 
        if user:
            
            # Clear any existing logins
            session.clear()

            # Set session cookie
            session['user_id'] = user[0]
            session['first_name'] = user[1]
            session['last_name'] = user[2]
            session['email'] = user[3]
            session['logged_in'] = True
            session['as_user'] = True
            
            return redirect('/user_account')

        # No match found: send back to login page
        else:
            return render_template(
                'pages/auth/user_login_page.html',
                logged_in=logged_in,
                as_user=as_user,
                message='Invalid entry. Please try again!'
            )