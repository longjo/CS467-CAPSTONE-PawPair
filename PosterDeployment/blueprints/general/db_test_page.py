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

    # Execute a query to select all Users
    query = """SELECT * FROM Users"""
    cursor.execute(query)
    users = cursor.fetchall()

    # Execute a query to select all Shelters
    query = """SELECT * FROM Shelters"""
    cursor.execute(query)
    shelters = cursor.fetchall()

    # Execute a query to select all Animals
    query = """SELECT * FROM Animals"""
    cursor.execute(query)
    animals = cursor.fetchall()

    # Execute a query to select all Animal Breeds
    query = """SELECT * FROM Animal_Breeds"""
    cursor.execute(query)
    animal_breeds = cursor.fetchall()

    # Execute a query to select all Animal Types
    query = """SELECT * FROM Animal_Types"""
    cursor.execute(query)
    animal_types = cursor.fetchall()

    # Execute a query to select all Dispositions
    query = """SELECT * FROM Dispositions"""
    cursor.execute(query)
    dispositions = cursor.fetchall()

    # Execute a query to select all Animal Dispositions sorted by animal_id
    query = """SELECT * FROM Animal_Dispositions ORDER BY animal_id"""
    cursor.execute(query)
    animal_dispositions = cursor.fetchall()

    # Close the cursor
    cursor.close()

    # Render the index template with the users
    return render_template(
        'db.html',
        users=users,
        shelters=shelters,
        animals=animals,
        animal_breeds=animal_breeds,
        animal_types=animal_types,
        dispositions=dispositions,
        animal_dispositions=animal_dispositions
    )