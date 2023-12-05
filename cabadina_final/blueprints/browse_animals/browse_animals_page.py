from flask import Blueprint, redirect, render_template, session, request

from utils import make_db_connection

browse_animals_bp = Blueprint('browse_animals', __name__, template_folder='templates')

@browse_animals_bp.route('/browse_animals', methods=['GET', 'POST'])
def browse_animals():
    # Check for login
    logged_in = session.get('logged_in', False)
    as_user = session.get('as_user', False)

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

    # Pull all shelter animals with type and breed names
    # from Animals, Animal_Types, and Animal_Breeds
    query = """
    SELECT DISTINCT
        Animals.animal_id,
        Animals.animal_name,
        Animal_Types.type_name,
        Animal_Breeds.breed_name,
        Animals.age,
        Animals.gender,
        Animals.image_url
    FROM Animals

    JOIN Animal_Types ON Animals.type_id = Animal_Types.type_id
    JOIN Animal_Breeds ON Animals.breed_id = Animal_Breeds.breed_id
    """
    # Check if any dispositions filter parameters are selected
    animal_dispositions = request.form.getlist('animal_dispositions')

    # Add necessary JOIN for dispositions
    if animal_dispositions:
        query += "JOIN Animal_Dispositions ON Animals.animal_id = Animal_Dispositions.animal_id\n"

    # Check if any basic filter parameters are passed
    filters = []
    if request.method == 'POST':
        animal_type = request.form.get('animal_type')
        animal_breed = request.form.get('animal_breed')
        age = request.form.get('age')
        gender = request.form.get('gender')
        availability = request.form.get('availability')

        # Add basic filters to the query if they are provided
        if animal_type:
            filters.append(f"Animals.type_id = '{animal_type}'")
        if animal_breed:
            filters.append(f"Animals.breed_id = '{animal_breed}'")
        if age:
            filters.append(f"Animals.age = '{age}'")
        if gender:
            filters.append(f"Animals.gender = '{gender}'")

        if availability:
            filters.append(f"Animals.availability = '{availability}'")
        else:
            filters.append(f"Animals.availability IN ('Available', 'Pending')")

        # Add disposition filters to the query if they are provided
        if animal_dispositions:
            filters.append("""
                Animals.animal_id IN (
                    SELECT animal_id
                    FROM Animal_Dispositions
                    WHERE disposition_id IN ({})
                    GROUP BY animal_id
                    HAVING COUNT(DISTINCT disposition_id) >= {}
                )
                """.format(','.join(animal_dispositions), len(animal_dispositions)))

    # Append any provided filters to query
    if filters:
        query += " WHERE " + " AND ".join(filters)

    # Apply sort filter
    sort_query = {
        'old': " ORDER BY Animals.animal_id;",
        'new': " ORDER BY Animals.animal_id DESC;",
        'name_asc': " ORDER BY Animals.animal_name;",
        'name_desc': " ORDER BY Animals.animal_name DESC;"
    }
    sort_by = request.form.get('sort_by', 'new')

    query += sort_query[sort_by]

    cursor.execute(query)
    animals = cursor.fetchall()

    # Close the cursor and the database connection
    cursor.close()
    db.close()

    return render_template(
        'pages/browse_animals/browse_animals_page.html',
        logged_in=logged_in,
        as_user=as_user,
        animals=animals,
        animal_types=animal_types,
        animal_breeds=animal_breeds,
        dispositions=dispositions
    )
