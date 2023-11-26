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

        # Create a db connection and cursor
        db = make_db_connection()
        cursor = db.cursor()

        # Execute a query to select all Animal Types
        query = """SELECT * FROM Animal_Types"""
        cursor.execute(query)
        animal_types = cursor.fetchall()

        # Execute a query to select all Animal Breeds
        query = """SELECT * FROM Animal_Breeds"""
        cursor.execute(query)
        animal_breeds = cursor.fetchall()

        # Execute a query to select all Dispositions
        query = """SELECT * FROM Dispositions"""
        cursor.execute(query)
        dispositions = cursor.fetchall()

        return render_template(
            'pages/shelter_animals/add_shelter_animal_page.html',
            logged_in=session.get('logged_in', False),
            as_user=session.get('as_user', False),
            animal_types=animal_types,
            animal_breeds=animal_breeds,
            dispositions=dispositions
        )
    
    # Write to DB
    if request.method == 'POST':

        # Get the form data
        animal_name = request.form['animal_name']
        animal_type = int(request.form['animal_type'])
        animal_breed = int(request.form['animal_breed'])
        age = request.form['age']
        gender = request.form['gender']
        dispositions = request.form.getlist('dispositions')
        image_url = request.form['image_url']
        description = request.form['description']
        news_item = request.form['news_item']
        availability = request.form['availability']

        # Get current shelter's ID 
        shelter_id = session.get('shelter_id')

        # Create a database connection
        db = make_db_connection()

        # Create a cursor
        cursor = db.cursor()

        # Insert the form data into the Animals database
        query = """
            INSERT INTO Animals (
                animal_name,
                type_id,
                breed_id,
                age,
                gender, 
                image_url,
                description,
                news_item,
                shelter_id,
                availability
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            animal_name,
            animal_type,
            animal_breed,
            age,
            gender,
            image_url,
            description,
            news_item,
            shelter_id,
            availability
            ))

        # Commit the changes
        db.commit()

        # Get the animal_id of the animal that was just created
        animal_id = cursor.lastrowid

        # Create entries in the Animal Dispositions table
        for disposition in dispositions:
            query = """
                INSERT INTO Animal_Dispositions (animal_id, disposition_id)
                VALUES (%s, %s)
            """
            cursor.execute(query, (animal_id, int(disposition)))
        
        # Commit the changes
        db.commit()

        # Close the cursor and the database connection
        cursor.close()
        db.close()

        return redirect('/shelter_account')