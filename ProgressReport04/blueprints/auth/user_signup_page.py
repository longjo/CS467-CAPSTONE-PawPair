from flask import Blueprint, redirect, render_template, request, session

from utils import make_db_connection

import mysql.connector

user_signup_page_bp = Blueprint('user_signup', __name__, template_folder='templates')

@user_signup_page_bp.route('/user_signup', methods=['GET', 'POST'])
def user_signup():

    # Redirect logged-in users to their account page
    logged_in=session.get('logged_in', False)
    as_user=session.get('as_user', False)

    if logged_in:
        if as_user:
            return redirect('/user_account')
        else:
            return redirect('/shelter_account')

    # GET: Display user signup page
    if request.method == 'GET':
        return render_template(
            'pages/auth/user_signup_page.html',
            logged_in=logged_in,
            as_user=as_user
        )
    
    # POST: Attempt user account creation
    if request.method == 'POST':

        # Get the form data
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']

        # Create a db connection and cursor
        db = make_db_connection()
        cursor = db.cursor()

        # Look for email match in all databases
        query = """
            SELECT email FROM Users
            WHERE email=%s
            UNION
            SELECT email FROM Shelters
            WHERE email=%s
        """
        cursor.execute(query, (email, email))
        match_found = cursor.fetchone()

        # Email already in use: return to signup page
        if match_found:

            # Close the connection
            cursor.close()
            db.close()

            # Return to signup page and retry
            return render_template(
                  'pages/auth/user_signup_page.html',
                  logged_in=logged_in,
                  as_user=as_user,
                  message='Email aleady in use. Please try again.'
                )

        # Insert form data into the Users database
        query = """
            INSERT INTO Users (firstname, lastname, email, password)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (firstname, lastname, email, password))
        db.commit()

        # Close the connection
        cursor.close()
        db.close()

        # Account created: send to user login page 
        return render_template(
            'pages/auth/user_login_page.html',
            logged_in=logged_in,
            as_user=as_user,
            message="Signup successful!"
        )