from flask import Blueprint, render_template, redirect, request, session

from utils import make_db_connection

animal_details_bp = Blueprint('animal_details', __name__, template_folder='templates')

@animal_details_bp.route('/animal_details/<int:animal_id>', methods=['GET', 'POST'])
def animal_details(animal_id):
    # Check for valid user login
    logged_in=session.get('logged_in', False),
    as_user=session.get('as_user', False)

    # if not logged_in or as_user:
    #     redirect('/shelter_login')

    # Create a database connection
    db = make_db_connection()

    # Create a cursor
    cursor = db.cursor()

    # Select target animal

    # Pull all shelter animals with type and breed names
    # from Animals, Animal_Types, and Animal_Breeds
    query = """
    SELECT
        Animals.animal_id,
        Animals.animal_name,
        Animal_Types.type_name,
        Animal_Breeds.breed_name,
        Animals.age,
        Animals.gender,
        Animals.image_url,
        Animals.description,
        Animals.news_item,
        Shelters.shelter_name,
        Animals.availability,
        Animals.reserved_by,
        Animals.date_created
    FROM Animals

    JOIN Animal_Types ON Animals.type_id = Animal_Types.type_id
    JOIN Animal_Breeds ON Animals.breed_id = Animal_Breeds.breed_id
    JOIN Shelters ON Animals.shelter_id = Shelters.shelter_id

    WHERE Animals.animal_id = %s
    """
    cursor.execute(query, (animal_id,))
    animal = cursor.fetchone()
    
    # Execute a query to find any dispositions
    # associated with the current animal
    query = """
        SELECT Dispositions.disposition_name
        FROM Dispositions
        JOIN Animal_Dispositions ON Dispositions.disposition_id = Animal_Dispositions.disposition_id
        WHERE Animal_Dispositions.animal_id = %s
    """
    cursor.execute(query, (animal_id,))
    data = cursor.fetchall()

    # Extract only disposition names
    animal_dispositions = [d[0] for d in data]

    # Close the cursor and the database connection
    cursor.close()
    db.close()

    # Display animal details page
    if request.method == 'GET':
        return render_template(
            'pages/browse_animals/animal_details_page.html',
            logged_in=session.get('logged_in', False),
            as_user=session.get('as_user', False),
            animal=animal,
            animal_dispositions=animal_dispositions
        )
    
    # Write to DB
    if request.method == 'POST':

        # Redirect non-users to the login page
        if not logged_in or not as_user:
            redirect('/login')

        # Collect form and user data
        action = request.form.get('action')
        user_id = session.get('user_id', -999)

        # Create a database connection
        db = make_db_connection()

        # Create a cursor
        cursor = db.cursor()

        # Update the Animals database to reflect reservation
        if action == 'reserve':
            query = """
                UPDATE Animals SET 
                    availability = "Pending",
                    reserved_by = %s
                WHERE animal_id = %s
            """
            cursor.execute(query, (user_id, animal_id))

        # Update the Animals database to reflect cancelled reservation
        if action == 'cancel':
            query = """
                UPDATE Animals SET 
                    availability = "Available",
                    reserved_by = NULL
                WHERE animal_id = %s
            """
            cursor.execute(query, (animal_id,))

        # Commit the changes
        db.commit()

        # Close the cursor and the database connection
        cursor.close()
        db.close()

        return redirect('/user_account')