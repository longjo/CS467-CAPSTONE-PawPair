from flask import Blueprint, redirect, render_template, session

from utils import make_db_connection

shelter_account_page_bp = Blueprint('shelter_account', __name__, template_folder='templates')

@shelter_account_page_bp.route('/shelter_account')
def shelter_account():
    # Check for valid shelter login
    logged_in=session.get('logged_in', False),
    as_user=session.get('as_user', False)

    if logged_in and not as_user:
        shelter_id = session['shelter_id']
        name = session['sheltername']
        email = session['email']
        zip = session['zip']

        # Create a database connection
        db = make_db_connection()

        # Create a cursor
        cursor = db.cursor()

        # Pull shelter animals from db
        query = """
            SELECT *
            FROM Animals
            WHERE shelter_id = %s
        """
        cursor.execute(query, (shelter_id,))
        animals = cursor.fetchall()

        # Close the cursor and the database connection
        cursor.close()
        db.close()

        # Display the shelter's information on the page.
        return render_template(
            'pages/shelter_account/shelter_account_page.html',
            logged_in=logged_in,
            as_user=as_user,
            name=name,
            email=email,
            zip=zip,
            animals=animals
        )
    else:
        return redirect('/shelter_login')