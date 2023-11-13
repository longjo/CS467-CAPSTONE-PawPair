from flask import Blueprint, render_template, request, session

from utils import make_db_connection

import mysql.connector

db_test_page_bp = Blueprint('db_test', __name__, template_folder='templates')


@db_test_page_bp.route('/testing')
def db_test():
    # Create a database connection
    db = make_db_connection()

    # Create a cursor
    cursor = db.cursor()

    # Execute a query to read all of the users from the users table
    query = """
        SELECT user_id, firstname, lastname, email, password
        FROM Users
    """
    cursor.execute(query)
        
    # Get the results of the query
    users = cursor.fetchall()

    # Execute a query to read all of the shelters from the shelters table
    query = """
        SELECT shelter_id, sheltername, email, zip, password
        FROM Shelters
    """
    cursor.execute(query)

    # Get the results of the query
    shelters = cursor.fetchall()

    # Execute a query to read all of the users from the users table
    query = """
        SELECT animal_id, name, species, breed, age, gender, image_url, description, shelter_id
        FROM Animals
    """
    cursor.execute(query)
        
    # Get the results of the query
    animals = cursor.fetchall()

    # Close the cursor
    cursor.close()

    # Render the index template with the users
    return render_template(
        'db.html',
        users=users,
        shelters=shelters,
        animals=animals
    )