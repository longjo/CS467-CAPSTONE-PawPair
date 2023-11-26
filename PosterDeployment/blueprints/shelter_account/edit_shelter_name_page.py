from flask import Blueprint,  redirect, render_template, request, session

from utils import make_db_connection

edit_shelter_name_page_bp = Blueprint('edit_shelter_name', __name__, template_folder='templates')

@edit_shelter_name_page_bp.route('/edit_shelter_name', methods=['GET', 'POST'])
def edit_name():

    # Display prefilled form
    if request.method == 'GET':
        if session.get('logged_in'):
            shelter_name = session['shelter_name']
            return render_template(
                'pages/shelter_account/edit_shelter_name_page.html',
                logged_in=session.get('logged_in', False),
                as_user=session.get('as_user', False),
                shelter_name=shelter_name
            )
        else:
            return redirect('/shelter_login')

    # Write to DB
    if request.method == 'POST':

        # Get the form data
        shelter_name = request.form['shelter_name']

        # Create a database connection
        db = make_db_connection()

        # Create a cursor
        cursor = db.cursor()

        # Insert the form data into the database
        query = """
            UPDATE Shelters
            SET shelter_name = %s
            WHERE shelter_id = %s
        """
        cursor.execute(query, (shelter_name, session.get('shelter_id', -999)))

        # Commit the changes
        db.commit()

        # Pull updated name from db
        query = """
            SELECT shelter_name
            FROM Shelters
            WHERE shelter_id = %s
        """
        cursor.execute(query, (session.get('shelter_id', -999),))
        shelter = cursor.fetchone()

        # Update session
        session['shelter_name'] = shelter[0]

        # Close the cursor and the database connection
        cursor.close()
        db.close()

        return redirect('/shelter_account')