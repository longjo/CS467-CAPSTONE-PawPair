from flask import Flask, render_template, request, redirect, url_for, session

import mysql.connector

app = Flask(__name__)

# Configure the database connection
app.config['MYSQL_HOST'] = 'XxXxXXXXxxxXxx'
app.config['MYSQL_USER'] = 'XxXxXXXXxxxXxx'
app.config['MYSQL_PASSWORD'] = 'XxXxXXXXxxxXxx'
app.config['MYSQL_DATABASE'] = 'XxXxXXXXxxxXxx'

# Configure security key with random string
app.config['SECRET_KEY'] = 'XxXxXXXXxxxXxx'


@app.route('/')
def home():
    return render_template('landing_page.html', logged_in=session.get('logged_in', False))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # Display signup page
    if request.method == 'GET':
        return render_template('signup_page.html', logged_in=session.get('logged_in', False))
    
    # Write to DB
    if request.method == 'POST':

        # Get the form data
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']

        # Create a database connection
        db = mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DATABASE']
        )

        # Create a cursor
        cursor = db.cursor()

        # Insert the form data into the database
        query = """
            INSERT INTO Users (firstname, lastname, email, password)
            VALUES (%s, %s, %s, %s)
        """

        try:
            cursor.execute(query, (firstname, lastname, email, password))

            # Commit the changes
            db.commit() 

        except mysql.connector.errors.IntegrityError:
              # Display an error message to the user indicating that the email address is already in use.
              return render_template('signup_page.html', logged_in=session.get('logged_in', False), error=True)


        # Close the cursor and the database connection
        cursor.close()
        db.close()

        return render_template('login_page.html', message="Signup successful!", logged_in=session.get('logged_in', False))


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Display signup page
    if request.method == 'GET':
        return render_template('login_page.html', logged_in=session.get('logged_in', False))
    
    # Read from DB
    if request.method == 'POST':

        # Get the form data
        email = request.form['email']
        password = request.form['password']

        # Create a database connection
        db = mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DATABASE']
        )

        # Create a cursor
        cursor = db.cursor()

        # Select user with matching username/password combination
        query = """
            SELECT * FROM Users
            WHERE email=%s AND password=%s
        """
        cursor.execute(query, (email, password))
        user = cursor.fetchone()

        # Close the cursor and the database connection
        cursor.close()
        db.close()

        # If match is found, set session cookie then redirect to landing page
        if user:
            session['user_id'] = user[0]
            session['first_name'] = user[1]
            session['last_name'] = user[2]
            session['email'] = user[3]
            session['logged_in'] = True
            return redirect('/')
        else:
            return render_template('login_page.html', message='Try again!', logged_in=session.get('logged_in', False))


# Define the account route
@app.route('/account')
def account():
    if session.get('logged_in'):
        name = f"{session['first_name']} {session['last_name']}"
        email = session['email']

        # Display the user's information on the page.
        return render_template('account_page.html', logged_in=session.get('logged_in', False), name=name, email=email)
    else:
        return redirect('/login')


# Define the edit name route
@app.route('/edit_name', methods=['GET', 'POST'])
def edit_name():

    # Display prefilled form
    if request.method == 'GET':
        if session.get('logged_in'):
            firstname = session['first_name']
            lastname = session['last_name']
            return render_template('edit_name_page.html', logged_in=session.get('logged_in', False), firstname=firstname, lastname=lastname)
        else:
            return redirect('/login')

    # Write to DB
    if request.method == 'POST':

        # Get the form data
        firstname = request.form['firstname']
        lastname = request.form['lastname']

        # Create a database connection
        db = mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DATABASE']
        )

        # Create a cursor
        cursor = db.cursor()

        # Insert the form data into the database
        query = """
            UPDATE Users
            SET firstname = %s, lastname = %s
            WHERE user_id = %s
        """
        cursor.execute(query, (firstname, lastname, session.get('user_id', -999)))

        # Commit the changes
        db.commit()

        # Pull updated name from db
        query = """
            SELECT firstname, lastname
            FROM Users
            WHERE user_id = %s
        """
        cursor.execute(query, (session.get('user_id', -999),))
        user = cursor.fetchone()

        # Update session
        session['first_name'] = user[0]
        session['last_name'] = user[1]

        # Close the cursor and the database connection
        cursor.close()
        db.close()

        return redirect('/account')



# Define the edit email route
@app.route('/edit_email', methods=['GET', 'POST'])
def edit_email():

    # Display prefilled form
    if request.method == 'GET':
        if session.get('logged_in'):
            email = session['email']
            return render_template('edit_email_page.html', logged_in=session.get('logged_in', False), email=email)
        else:
            return redirect('/login')

    # Write to DB
    if request.method == 'POST':

        # Get the form data
        email = request.form['email']

        # Create a database connection
        db = mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DATABASE']
        )

        # Create a cursor
        cursor = db.cursor()

        # Insert the form data into the database
        query = """
            UPDATE Users
            SET email = %s
            WHERE user_id = %s
        """

        try:
            cursor.execute(query, (email, session.get('user_id', -999)))

            # Commit the changes
            db.commit() 

        except mysql.connector.errors.IntegrityError:
              # Display an error message to the user indicating that the email address is already in use.
              return render_template('edit_email_page.html', logged_in=session.get('logged_in', False), email=email, error=True)


        # Pull updated email from db
        query = """
            SELECT email
            FROM Users
            WHERE user_id = %s
        """
        cursor.execute(query, (session.get('user_id', -999),))
        user = cursor.fetchone()

        # Update session
        session['email'] = user[0]

        # Close the cursor and the database connection
        cursor.close()
        db.close()

        return redirect('/account')



# Define the edit password route
@app.route('/change_password', methods=['GET', 'POST'])
def change_password():

    # Display prefilled form
    if request.method == 'GET':
        return render_template('change_password_page.html', logged_in=session.get('logged_in', False))

    # Write to DB
    if request.method == 'POST':

        # Get the form data
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        new_password_check = request.form['new_password_check']

        if new_password != new_password_check:
            return render_template('change_password_page.html', logged_in=session.get('logged_in', False), error=True)

        # Create a database connection
        db = mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DATABASE']
        )

        # Create a cursor
        cursor = db.cursor()

        # Select password of current user
        query = """
            SELECT password FROM Users
            WHERE user_id=%s
        """
        cursor.execute(query, (session.get('user_id', -999),))
        user_password = cursor.fetchone()

        # If provided password doesn't match
        if current_password != user_password[0]:

            # Close the cursor and the database connection
            cursor.close()
            db.close()

            # Go back and indicate the error    
            return render_template('change_password_page.html', logged_in=session.get('logged_in', False), error=True)

        else:
            # Insert the new password into the database
            query = """
                UPDATE Users
                SET password = %s
                WHERE user_id = %s
            """
            cursor.execute(query, (new_password, session.get('user_id', -999)))

            # Commit the changes
            db.commit()
            
            # Close the cursor and the database connection
            cursor.close()
            db.close()

            return redirect('/account')

        

# Define the logout route
@app.route('/delete_account', methods=['GET', 'POST'])
def delete_account():

    # Display prefilled form
    if request.method == 'GET':
        if session.get('logged_in'):
            return render_template('delete_account_page.html', logged_in=session.get('logged_in', False))
        else:
            return redirect('/login')

    # Delete account from DB
    if request.method == 'POST':

        # Get the form data
        password = request.form['password']

        # Create a database connection
        db = mysql.connector.connect(
            host=app.config['MYSQL_HOST'],
            user=app.config['MYSQL_USER'],
            password=app.config['MYSQL_PASSWORD'],
            database=app.config['MYSQL_DATABASE']
        )

        # Create a cursor
        cursor = db.cursor()

        # Select user with matching username/password combination
        query = """
            SELECT password FROM Users
            WHERE user_id=%s
        """
        cursor.execute(query, (session.get('user_id', -999),))
        user_password = cursor.fetchone()

        
        # If provided password matches or is '123'...
        if password == user_password[0] or password == '123':

            # Delete the form data into the database
            query = """
                DELETE FROM Users
                WHERE user_id = %s
            """
            cursor.execute(query, (session.get('user_id', -999),))

            # Commit the changes
            db.commit() 

            # Clear the user's session
            session.clear()
            return redirect('/')

        # Close the cursor and the database connection
        cursor.close()
        db.close()

        return redirect('/delete_account')




# Define the logout route
@app.route('/logout')
def logout():
    # Clear the user's session
    session.clear()
    return redirect('/')


@app.route('/testing')
def testing():
    # Create a database connection
    db = mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DATABASE']
    )

    # Create a cursor
    cursor = db.cursor()

    # Execute a query to read all of the users from the users table
    # cursor.execute("SELECT * FROM Users")
    query = """
        SELECT user_id, firstname, lastname, email, password
        FROM Users
    """
    cursor.execute(query)
        
    # Get the results of the query
    data = cursor.fetchall()

    # Close the cursor
    cursor.close()

    # Render the index template with the users
    return render_template('db.j2', data=data)
    # return data

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=5000)