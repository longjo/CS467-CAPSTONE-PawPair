from flask import Blueprint,  redirect, render_template, request, session

from utils import make_db_connection

import mysql.connector

edit_user_email_page_bp = Blueprint('edit_user_email', __name__, template_folder='templates')

@edit_user_email_page_bp.route('/edit_user_email', methods=['GET', 'POST'])
def edit_user_email():

    # Display prefilled form
    if request.method == 'GET':
        if session.get('logged_in'):
            email = session['email']
            return render_template(
                'pages/user_account/edit_user_email_page.html',
                logged_in=session.get('logged_in', False),
                as_user=session.get('as_user', False),
                email=email
            )
        else:
            return redirect('/user_login')

    # Write to DB
    if request.method == 'POST':

        # Get the form data
        email = request.form['email']

        # Create a database connection
        db = make_db_connection()

        # Create a cursor
        cursor = db.cursor()

        # Look for email match in Shelters database
        query = """
            SELECT * FROM Shelters
            WHERE email=%s
        """
        cursor.execute(query, (email,))
        match = cursor.fetchone()

        # If email already in use, send user back to edit email page
        if match:
            return render_template(
                'pages/user_account/edit_user_email_page.html',
                logged_in=session.get('logged_in', False),
                as_user=session.get('as_user', False),
                email=email,
                error=True
            )

        # Insert the form data into the database
        query = """
            UPDATE Users
            SET email = %s
            WHERE user_id = %s
        """

        try:
            cursor.execute(query, (email, session.get('user_id', -999)))

            # Commit the changes
            db.commit() 

        except mysql.connector.errors.IntegrityError:
            # Display an error message to the user indicating that the email address is already in use.
            return render_template(
                'pages/user_account/edit_user_email_page.html',
                logged_in=session.get('logged_in', False),
                as_user=session.get('as_user', False),
                email=email,
                error=True
            )

        # Pull updated email from db
        query = """
            SELECT email
            FROM Users
            WHERE user_id = %s
        """
        cursor.execute(query, (session.get('user_id', -999),))
        user = cursor.fetchone()

        # Update session
        session['email'] = user[0]

        # Close the cursor and the database connection
        cursor.close()
        db.close()

        return redirect('/user_account')
