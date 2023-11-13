from flask import Blueprint,  redirect, render_template, request, session

from utils import make_db_connection

import mysql.connector

edit_shelter_email_page_bp = Blueprint('edit_shelter_email', __name__, template_folder='templates')

@edit_shelter_email_page_bp.route('/edit_shelter_email', methods=['GET', 'POST'])
def edit_shelter_email():

    # Display prefilled form
    if request.method == 'GET':
        if session.get('logged_in'):
            email = session['email']
            return render_template(
                'pages/shelter_account/edit_shelter_email_page.html',
                logged_in=session.get('logged_in', False),
                as_user=session.get('as_user', False),
                email=email
            )
        else:
            return redirect('/shelter_login')

    # Write to DB
    if request.method == 'POST':

        # Get the form data
        email = request.form['email']

        # Create a database connection
        db = make_db_connection()

        # Create a cursor
        cursor = db.cursor()

        # Look for email match in Users database
        query = """
            SELECT * FROM Users
            WHERE email=%s
        """
        cursor.execute(query, (email,))
        match = cursor.fetchone()

        # If email already in use, send user back to edit email page
        if match:
            return render_template(
                'pages/shelter_account/edit_shelter_email_page.html',
                logged_in=session.get('logged_in', False),
                as_user=session.get('as_user', False),
                email=email,
                error=True
            )

        # Insert the form data into the Shelters database
        query = """
            UPDATE Shelters
            SET email = %s
            WHERE shelter_id = %s
        """

        try:
            cursor.execute(query, (email, session.get('shelter_id', -999)))

            # Commit the changes
            db.commit() 

        except mysql.connector.errors.IntegrityError:
            # Display an error message to the shelter indicating that the email address is already in use.
            return render_template(
                'pages/shelter_account/edit_shelter_email_page.html',
                logged_in=session.get('logged_in', False),
                as_user=session.get('as_user', False),
                email=email,
                error=True
            )

        # Pull updated email from db
        query = """
            SELECT email
            FROM Shelters
            WHERE shelter_id = %s
        """
        cursor.execute(query, (session.get('shelter_id', -999),))
        shelter = cursor.fetchone()

        # Update session
        session['email'] = shelter[0]

        # Close the cursor and the database connection
        cursor.close()
        db.close()

        return redirect('/shelter_account')
