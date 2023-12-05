from flask import Blueprint, redirect, render_template, request, session

from utils import make_db_connection

login_page_bp = Blueprint('login', __name__, template_folder='templates')


@login_page_bp.route('/login', methods=['GET', 'POST'])
def login():

    # Redirect already logged in users
    logged_in=session.get('logged_in', False)
    as_user=session.get('as_user', False)

    if logged_in:
        if as_user:
            return redirect('/user_account')
        else:
            return redirect('/shelter_account')

    # GET: Display shelter login page
    if request.method == 'GET':
        return render_template(
            'pages/auth/login_page.html',
            logged_in=logged_in,
            as_user=as_user
        )
    
    # POST: Attempt login
    if request.method == 'POST':

        # Get the form data
        email = request.form['email']
        password = request.form['password']

        # Create a db connection and cursor
        db = make_db_connection()
        cursor = db.cursor()

        # Check login credentials against Users db
        query = """
            SELECT * FROM Users
            WHERE email=%s AND password=%s
        """
        cursor.execute(query, (email, password))
        user = cursor.fetchone()

        # Credentials match: log in then send to user account page 
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


        # No match found: check for Shelter login

        # Check login credentials against Shelters db
        query = """
            SELECT * FROM Shelters
            WHERE email=%s AND password=%s
        """
        cursor.execute(query, (email, password))
        shelter = cursor.fetchone()

        # Close the connection
        cursor.close()
        db.close()

        # Credentials match: log in then send to shelter account page 
        if shelter:
            
            # Clear any existing logins
            session.clear()

            # Set session cookie
            session['shelter_id'] = shelter[0]
            session['shelter_name'] = shelter[1]
            session['email'] = shelter[2]
            session['zip'] = shelter[3]
            session['logged_in'] = True
            session['as_user'] = False

            return redirect('/shelter_account')
        
        # No matches found: send back to login page
        else:
            return render_template(
                'pages/auth/login_page.html',
                logged_in=logged_in,
                as_user=as_user,
                message='Invalid entry. Please try again!'
            )