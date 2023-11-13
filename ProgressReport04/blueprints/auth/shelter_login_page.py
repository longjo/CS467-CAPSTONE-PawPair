from flask import Blueprint, redirect, render_template, request, session

from utils import make_db_connection

shelter_login_page_bp = Blueprint('shelter_login', __name__, template_folder='templates')


@shelter_login_page_bp.route('/shelter_login', methods=['GET', 'POST'])
def shelter_login():

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
            'pages/auth/shelter_login_page.html',
            logged_in=logged_in,
            as_user=as_user
        )
    
    # POST: Attempt shelter login 
    if request.method == 'POST':

        # Get the form data
        email = request.form['email']
        password = request.form['password']

        # Create a db connection and cursor
        db = make_db_connection()
        cursor = db.cursor()

        # Verify login credentials match stored data
        query = """
            SELECT * FROM Shelters
            WHERE email=%s AND password=%s
        """
        cursor.execute(query, (email, password))
        shelter = cursor.fetchone()

        # Close the connection
        cursor.close()
        db.close()

        # Credentials match: log in then send to account page 
        if shelter:
            
            # Clear any existing logins
            session.clear()

            # Set session cookie
            session['shelter_id'] = shelter[0]
            session['sheltername'] = shelter[1]
            session['email'] = shelter[2]
            session['zip'] = shelter[4]
            session['logged_in'] = True
            session['as_user'] = False

            return redirect('/shelter_account')
        
        # No match found: send back to login page
        else:
            return render_template(
                'pages/auth/shelter_login_page.html',
                logged_in=logged_in,
                as_user=as_user,
                message='Invalid entry. Please try again!'
            )