from flask import Blueprint, render_template, redirect, request, session

from utils import make_db_connection

delete_shelter_animal_bp = Blueprint('delete_shelter_animal', __name__, template_folder='templates')

@delete_shelter_animal_bp.route('/delete_shelter_animal/<int:animal_id>')
def edit_shelter_animal(animal_id):
    # Check for valid shelter login
    logged_in=session.get('logged_in', False),
    as_user=session.get('as_user', False)

    if not logged_in or as_user:
        redirect('/shelter_login')

    # Create a database connection
    db = make_db_connection()

    # Create a cursor
    cursor = db.cursor()

    # Select target animal
    query = """
        SELECT * FROM Animals
        WHERE animal_id = %s
    """
    cursor.execute(query, (animal_id,))
    animal = cursor.fetchone()

    # Stop if animal is not associated with current shelter
    animal_shelter_id = animal[8]
    if animal_shelter_id != session.get('shelter_id', -999):

        # Close the cursor and the database connection
        cursor.close()
        db.close()

        # Return to account page
        return redirect('/shelter_account')
    
    # Otherwise, continue with deletion
    query = """
        DELETE FROM Animals
        WHERE animal_id = %s
    """
    cursor.execute(query, (animal_id,))

    # Commit the changes
    db.commit()

    # Close the cursor and the database connection
    cursor.close()
    db.close()

    return redirect('/shelter_account')