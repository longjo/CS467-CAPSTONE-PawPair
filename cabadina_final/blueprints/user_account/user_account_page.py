from flask import Blueprint, redirect, render_template, session

from utils import make_db_connection

user_account_page_bp = Blueprint('user_account', __name__, template_folder='templates')

@user_account_page_bp.route('/user_account')
def user_account():
    if session.get('logged_in'):
        user_name = f"{session['first_name']} {session['last_name']}"
        email = session['email']

        # Create a db connection and cursor
        db = make_db_connection()
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
            Animals.image_url
        FROM Animals
        JOIN Animal_Types ON Animals.type_id = Animal_Types.type_id
        JOIN Animal_Breeds ON Animals.breed_id = Animal_Breeds.breed_id
        WHERE Animals.reserved_by = %s
        """

        cursor.execute(query, (session.get('user_id', -999),))
        animals = cursor.fetchall()

        # Close the cursor and the database connection
        cursor.close()
        db.close()


        # Display the user's information on the page.
        return render_template(
            'pages/user_account/user_account_page.html',
            logged_in=session.get('logged_in', False),
            as_user=session.get('as_user', False),
            user_name=user_name,
            email=email,
            animals=animals
        )
    else:
        return redirect('/user_login')