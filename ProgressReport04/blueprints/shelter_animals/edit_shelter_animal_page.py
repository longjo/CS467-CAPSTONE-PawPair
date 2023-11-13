from flask import Blueprint, render_template, redirect, request, session

from utils import make_db_connection

edit_shelter_animal_bp = Blueprint('edit_shelter_animal', __name__, template_folder='templates')

@edit_shelter_animal_bp.route('/edit_shelter_animal/<int:animal_id>', methods=['GET', 'POST'])
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

    # Close the cursor and the database connection
    cursor.close()
    db.close()

    # Stop if animal is not associated with current shelter
    animal_shelter_id = animal[8]
    if animal_shelter_id != session.get('shelter_id', -999):

        # Return to account page
        return redirect('/shelter_account')
    
    # Otherwise, display edit animal page
    if request.method == 'GET':
        return render_template(
            'pages/shelter_animals/edit_shelter_animal_page.html',
            logged_in=session.get('logged_in', False),
            as_user=session.get('as_user', False),
            animal=animal
        )
    
    # Write to DB
    if request.method == 'POST':

        # Get the form data
        name = request.form['name']
        species = request.form['species']
        breed = request.form['breed']   
        age = request.form['age']
        gender = request.form['gender']
        image_url = request.form['image_url']
        description = request.form['description']

        # Account for empty image URL
        if image_url == "":
            image_url = 'static/images/default_animal_image.png'

        # Get current shelter's ID 
        shelter_id = session.get('shelter_id')

        # Create a database connection
        db = make_db_connection()

        # Create a cursor
        cursor = db.cursor()

        # Insert the form data into the Animals database
        query = """
            UPDATE Animals
            SET name = %s,
                species = %s,
                breed = %s,
                age = %s,
                gender = %s,
                image_url = %s,
                description = %s,
                shelter_id = %s
            WHERE animal_id = %s
        """
        cursor.execute(
            query,
            (name, species, breed, age, gender, image_url, description, shelter_id, animal_id)
        )

        # Commit the changes
        db.commit()

        # Close the cursor and the database connection
        cursor.close()
        db.close()

        return redirect('/shelter_account')