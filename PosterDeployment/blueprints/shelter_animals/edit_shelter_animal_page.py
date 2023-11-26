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

    # Stop if animal is not associated with current shelter
    animal_shelter_id = animal[9]
    if animal_shelter_id != session.get('shelter_id', -999):

        # Close the cursor and the database connection
        cursor.close()
        db.close()

        # Return to account page
        return redirect('/shelter_account')
    
    # Otherwise, collect the necessary table rows

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

    # Execute a query to find any dispositions
    # associated with the current animal
    query = """
        SELECT disposition_id FROM Animal_Dispositions
        WHERE animal_id = %s
    """
    cursor.execute(query, (animal_id,))
    data = cursor.fetchall()

    # Extract only disposition id's
    animal_dispositions = [d[0] for d in data]

    # Close the cursor and the database connection
    cursor.close()
    db.close()

    # Display edit animal page
    if request.method == 'GET':
        return render_template(
            'pages/shelter_animals/edit_shelter_animal_page.html',
            logged_in=session.get('logged_in', False),
            as_user=session.get('as_user', False),
            animal=animal,
            animal_types=animal_types,
            animal_breeds=animal_breeds,
            dispositions=dispositions,
            animal_dispositions=animal_dispositions
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

        # Account for empty news_item
        if news_item == "":
            news_item = None

        # Account for empty news_item
        if image_url == "":
            image_url = None

        # Handle Pending
        if availability == "Pending" or availability == "Adopted":
            reserved_by = animal[11]
        else:
            reserved_by = None

        # Update the Animals database with the form data
        query = """
            UPDATE Animals SET
                animal_name = %s,
                type_id = %s,
                breed_id = %s,
                age = %s,
                gender = %s,
                image_url = %s, 
                description = %s,
                news_item = %s,
                shelter_id = %s,
                availability = %s,
                reserved_by = %s
            WHERE animal_id = %s
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
            availability,
            reserved_by,
            animal_id
            ))

        # Commit the changes
        db.commit()





        # Delete existing entries from the Animal Dispositions table
        query = """
            DELETE FROM Animal_Dispositions
            WHERE animal_id = %s
        """
        cursor.execute(query, (animal_id,))

        # Create updated entries in the Animal Dispositions table
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