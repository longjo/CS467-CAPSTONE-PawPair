from flask import Blueprint, redirect, render_template, session

from utils import make_db_connection

shelter_account_page_bp = Blueprint('shelter_account', __name__, template_folder='templates')

@shelter_account_page_bp.route('/shelter_account')
def shelter_account():
    # Check for valid shelter login
    logged_in=session.get('logged_in', False),
    as_user=session.get('as_user', False)

    if logged_in and not as_user:
        shelter_id = session['shelter_id']
        shelter_name = session['shelter_name']
        email = session['email']
        zip = session['zip']

        # Create a database connection
        db = make_db_connection()

        # Create a cursor
        cursor = db.cursor()

        # Pull user's animals from db
        query = """
        SELECT
            Animals.animal_id,
            Animals.animal_name,
            Animal_Types.type_name,
            Animal_Breeds.breed_name,
            Animals.age,
            Animals.gender,
            Animals.image_url,
            COALESCE(Users.email, NULL) AS email,
            Animals.availability
        FROM Animals
        JOIN Animal_Types ON Animals.type_id = Animal_Types.type_id
        JOIN Animal_Breeds ON Animals.breed_id = Animal_Breeds.breed_id
        LEFT JOIN Users ON Animals.reserved_by = Users.user_id
        WHERE shelter_id = %s
        ORDER BY COALESCE(Animals.reserved_by, Animals.animal_id), Animals.animal_id
        """
        cursor.execute(query, (shelter_id,))
        animals = cursor.fetchall()

        # Close the cursor and the database connection
        cursor.close()
        db.close()

        # Display the shelter's information on the page.
        return render_template(
            'pages/shelter_account/shelter_account_page.html',
            logged_in=logged_in,
            as_user=as_user,
            shelter_name=shelter_name,
            email=email,
            zip=zip,
            animals=animals
        )
    else:
        return redirect('/shelter_login')