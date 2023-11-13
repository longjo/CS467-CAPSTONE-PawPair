from flask import Blueprint,  redirect, render_template, request, session

from utils import make_db_connection

edit_shelter_zip_page_bp = Blueprint('edit_shelter_zip', __name__, template_folder='templates')

@edit_shelter_zip_page_bp.route('/edit_shelter_zip', methods=['GET', 'POST'])
def edit_zip():

    # Display prefilled form
    if request.method == 'GET':
        if session.get('logged_in'):
            zip = session['zip']
            return render_template(
                'pages/shelter_account/edit_shelter_zip_page.html',
                logged_in=session.get('logged_in', False),
                as_user=session.get('as_user', False),
                zip=zip
            )
        else:
            return redirect('/shelter_login')

    # Write to DB
    if request.method == 'POST':

        # Get the form data
        zip = request.form['zip']

        # Create a database connection
        db = make_db_connection()

        # Create a cursor
        cursor = db.cursor()

        # Insert the form data into the database
        query = """
            UPDATE Shelters
            SET zip = %s
            WHERE shelter_id = %s
        """
        cursor.execute(query, (zip, session.get('shelter_id', -999)))

        # Commit the changes
        db.commit()

        # Pull updated zip from db
        query = """
            SELECT zip
            FROM Shelters
            WHERE shelter_id = %s
        """
        cursor.execute(query, (session.get('shelter_id', -999),))
        shelter = cursor.fetchone()

        # Update session
        session['zip'] = shelter[0]

        # Close the cursor and the database connection
        cursor.close()
        db.close()

        return redirect('/shelter_account')