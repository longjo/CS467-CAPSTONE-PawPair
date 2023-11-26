from flask import Blueprint,  redirect, render_template, request, session

from utils import make_db_connection

edit_user_name_page_bp = Blueprint('edit_user_name', __name__, template_folder='templates')

@edit_user_name_page_bp.route('/edit_user_name', methods=['GET', 'POST'])
def edit_name():

    # Display prefilled form
    if request.method == 'GET':
        if session.get('logged_in'):
            first_name = session['first_name']
            last_name = session['last_name']
            return render_template(
                'pages/user_account/edit_user_name_page.html',
                logged_in=session.get('logged_in', False),
                as_user=session.get('as_user', False),
                first_name=first_name,
                last_name=last_name
            )
        else:
            return redirect('/user_login')

    # Write to DB
    if request.method == 'POST':

        # Get the form data
        first_name = request.form['first_name']
        last_name = request.form['last_name']

        # Create a database connection
        db = make_db_connection()

        # Create a cursor
        cursor = db.cursor()

        # Insert the form data into the database
        query = """
            UPDATE Users
            SET first_name = %s, last_name = %s
            WHERE user_id = %s
        """
        cursor.execute(query, (first_name, last_name, session.get('user_id', -999)))

        # Commit the changes
        db.commit()

        # Pull updated name from db
        query = """
            SELECT first_name, last_name
            FROM Users
            WHERE user_id = %s
        """
        cursor.execute(query, (session.get('user_id', -999),))
        user = cursor.fetchone()

        # Update session
        session['first_name'] = user[0]
        session['last_name'] = user[1]

        # Close the cursor and the database connection
        cursor.close()
        db.close()

        return redirect('/user_account')