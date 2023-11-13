from flask import Blueprint, render_template, redirect, request, session

from utils import make_db_connection

add_shelter_animal_bp = Blueprint('add_shelter_animal', __name__, template_folder='templates')

@add_shelter_animal_bp.route('/add_shelter_animal', methods=['GET', 'POST'])
def add_shelter_animal():
    # Check for valid shelter login
    logged_in=session.get('logged_in', False),
    as_user=session.get('as_user', False)

    if not logged_in or as_user:
        redirect('/shelter_login')

    # Display add animal page
    if request.method == 'GET':
        return render_template(
            'pages/shelter_animals/add_shelter_animal_page.html',
            logged_in=session.get('logged_in', False),
            as_user=session.get('as_user', False)
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
            INSERT INTO Animals (name, species, breed, age, gender, image_url, description, shelter_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (name, species, breed, age, gender, image_url, description, shelter_id))

        # Commit the changes
        db.commit()

        # Close the cursor and the database connection
        cursor.close()
        db.close()

        return redirect('/shelter_account')