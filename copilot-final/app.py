# import Flask, render_template, request, redirect, session
from flask import Flask, render_template, request, redirect, session

# import boto3, Key, Attr
import boto3
from boto3.dynamodb.conditions import Key, Attr

# import access key and secret key from config.py
from config import ACCESS_KEY, SECRET_KEY


# connect to dynamodb: us-west-2, ACCESS_KEY, SECRET_KEY
dynamodb = boto3.resource('dynamodb', region_name='us-west-2', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

# create flask app with secret key = "secret"
app = Flask(__name__)
app.secret_key = 'secret'

# route to index page
# render index.j2 if not in session
# render loggedindex.j2 if in session
# render adminindex.j2 if in session as "admin"
@app.route('/')
def index():
    # if "id" not in session
    if 'id' not in session:
        # render index.j2
        return render_template('index.j2')
    # if "id" in session
    else:
        # if "id" in session as "admin"
        if session['id'] == 'admin':
            # render adminindex.j2
            return render_template('adminindex.j2')
        # if "id" in session as "user"
        else:
            # render loggedindex.j2
            return render_template('loggedindex.j2')

# route to login page with GET and POST methods
# GET: redirect to profile page if in session
# GET: render login.j2 with data from dynamodb table "users" if not in session
# POST: update session and redirect to index page if user submits: "id" and "pw" found in dynamodb table "users"
# POST: redirect to login page if user submits: "id" and "pw" not found in dynamodb table "users"
@app.route('/login', methods=['GET', 'POST'])
def login():
    # get table "users" from dynamodb
    table = dynamodb.Table('users')
    # if method is GET
    if request.method == 'GET':
        # if "id" in session
        if 'id' in session:
            # redirect to profile page
            return redirect('/profile')
        # if "id" not in session
        else:
            # get all items from table "users"
            response = table.scan()
            # render login.j2 with data from table "users"
            return render_template('login.j2', data=response['Items'])
    # if method is POST
    else:
        # get "id" and "pw" from form
        id = request.form['id']
        pw = request.form['pw']
        # get all items from table "users" where id = <id>
        response = table.query(
            KeyConditionExpression=Key('id').eq(id)
        )
        # if "id" and "pw" found in table "users"
        if response['Items'][0]['id'] == id and response['Items'][0]['pw'] == pw:
            # update session
            session['id'] = id
            # redirect to index page
            return redirect('/')
        # if "id" and "pw" not found in table "users"
        else:
            # redirect to login page
            return redirect('/login')

# route for logout
# clear session and redirect to index page
@app.route('/logout')
def logout():
    # clear session
    session.clear()
    # redirect to index page
    return redirect('/')

# route to create page with GET and POST methods
# GET: render create.j2 if not in session
# GET: render profile.j2 if in session
# POST: redirect to login page if user submits: "id", "pw", "fav" not in dynamodb table "users"
@app.route('/create', methods=['GET', 'POST'])
def create():
    # get table "users" from dynamodb
    table = dynamodb.Table('users')
    # if method is GET
    if request.method == 'GET':
        # if "id" not in session
        if 'id' not in session:
            # render create.j2
            return render_template('create.j2')
        # if "id" in session
        else:
            # render profile.j2
            return render_template('profile.j2')
    # if method is POST
    else:
        # get "id", "pw", "fav" from form
        id = request.form['id']
        pw = request.form['pw']
        fav = request.form['fav']
        # get all items from table "users" where id = <id>
        response = table.query(
            KeyConditionExpression=Key('id').eq(id)
        )
        # if "id" and "pw" not found in table "users"
        if response['Items'] == []:
            # put item into table "users"
            table.put_item(
                Item={
                    'id': id,
                    'pw': pw,
                    'fav': fav
                }
            )
            # redirect to login page
            return redirect('/login')
        # if "id" and "pw" found in table "users"
        else:
            # redirect to create page
            return redirect('/create')

# route to profile page
# render profile.j2 if in session
# render with session id information from dynamoDB table "users"
# render with animal data from dynamoDB table "animals"
@app.route('/profile')
def profile():
    # get table "users" from dynamodb
    table = dynamodb.Table('users')
    # get table "animals" from dynamodb
    table2 = dynamodb.Table('animals')
    # if "id" in session
    if 'id' in session:
        # get all items from table "users" where id = <id>
        response = table.query(
            KeyConditionExpression=Key('id').eq(session['id'])
        )
        # get all items from table "animals" where pending = <id>
        response2 = table2.scan(
            FilterExpression=Attr('pending').eq(session['id'])
        )
        # get all items from table "animals" where adopted = <id>
        response3 = table2.scan(
            FilterExpression=Attr('adopted').eq(session['id'])
        )
        # render profile.j2 with data from table "users" and table "animals"
        return render_template('profile.j2', data=response['Items'], data2=response2['Items'], data3=response3['Items'])
    # if "id" not in session
    else:
        # redirect to login page
        return redirect('/login')

# route to animals page with GET and POST methods
# GET: render animals.j2 with data from dynamodb table "animals" if not in session
# GET: render adminanimals.j2 with data from dynamodb table "animals" if in session as "admin"
# POST: "add" form: only allow if in session as "admin"
# POST: "add" form: redirect to animals page if user submits: "animal_id", "image", "animal", "breed", "disposition[]", "create_date", "availability", "pending", and "adopted" for dynamodb table "animals"
# POST: "search" form: redirect to animals page based on user input querying dynamodb table "animals" for "animal", "breed", "disposition[]", and "availability"
# POST: redirect to animals page
@app.route('/animals', methods=['GET', 'POST'])
def animals():
    # get table "animals" from dynamodb
    table = dynamodb.Table('animals')
    # if method is GET
    if request.method == 'GET':
        # if "id" not in session
        if 'id' not in session:
            # get all items from table "animals"
            response = table.scan()
            # render animals.j2 with data from table "animals"
            # pass flag to avoid showing "Show All Animals" button
            return render_template('animals.j2', data=response['Items'], flag=1)
        # if "id" in session
        else:
            # get all items from table "animals"
            response = table.scan()
            # if "id" in session as "admin"
            if session['id'] == 'admin':
                # create a list of "animal_id" from table "animals"
                animal_id_list = []
                for item in response['Items']:
                    animal_id_list.append(item['animal_id'])
                # find the smallest integer not in animal_id_list
                animal_id = 1
                while animal_id in animal_id_list:
                    animal_id += 1
                # render adminanimals.j2 with data from table "animals"
                # pass animal_id
                # pass flag to avoid showing "Show All Animals" button
                return render_template('adminanimals.j2', data=response['Items'], animal_id=animal_id, flag=1)
            # if "id" in session as "user"
            else:
                # render animalslogged.j2 with data from table "animals"
                # pass flag to avoid showing "Show All Animals" button
                return render_template('loggedanimals.j2', data=response['Items'], flag=1)
    # if method is POST
    else:
        # if form is "add"
        if request.form.get('add'):
            # if "id" in session as "admin"
            if session['id'] == 'admin':
                # get "animal_id", "image", "animal", "breed", "disposition[]", "create_date", and "availability" from form
                animal_id = int(request.form['animal_id'])
                image = request.form['image']
                animal = request.form['animal']
                breed = request.form['breed']
                disposition = request.form.getlist('disposition[]')
                create_date = request.form['create_date']
                availability = request.form['availability']
                # set pending and adopted to ""
                pending = "admin"
                adopted = "admin"
                # put item into table "animals"
                # include pending and adopted
                table.put_item(
                    Item={
                        'animal_id': animal_id,
                        'image': image,
                        'animal': animal,
                        'breed': breed,
                        'disposition': disposition,
                        'create_date': create_date,
                        'availability': availability,
                        'pending': pending,
                        'adopted': adopted
                    }
                )
                # redirect to animals page
                return redirect('/animals')
            # if "id" not in session as "admin"
            else:
                # redirect to animals page
                return redirect('/animals')
        # if form is "search"
        elif request.form.get('search'):
            # check if "animal", "breed", "disposition[]", and "availability" from form exist
            # if not, set to empty string or list
            if 'animal' in request.form:
                animal = request.form['animal']
            else:
                animal = ''
            # if breed is "No Preference", set to empty string
            if 'breed' in request.form:
                breed = request.form['breed']
                if breed == 'No Preference':
                    breed = ''
            else:
                breed = ''
            if 'disposition[]' in request.form:
                disposition = request.form.getlist('disposition[]')
            else:
                disposition = []
            # if breed is "No Preference", set to empty string
            if 'availability' in request.form:
                availability = request.form['availability']
                if availability == 'No Preference':
                    availability = ''
            else:
                availability = ''
            # get all items from table "animals" where animal = <animal>, breed = <breed>, disposition = <disposition>, and availability = <availability>
            # skip any of the above if they are empty
            if animal != '' and breed != '' and disposition != [] and availability != '':
                response = table.scan(
                    FilterExpression=Attr('animal').eq(animal) & Attr('breed').eq(breed) & Attr('disposition').eq(disposition) & Attr('availability').eq(availability)
                )
            elif animal != '' and breed != '' and disposition != [] and availability == '':
                response = table.scan(
                    FilterExpression=Attr('animal').eq(animal) & Attr('breed').eq(breed) & Attr('disposition').eq(disposition)
                )
            elif animal != '' and breed != '' and disposition == [] and availability != '':
                response = table.scan(
                    FilterExpression=Attr('animal').eq(animal) & Attr('breed').eq(breed) & Attr('availability').eq(availability)
                )
            elif animal != '' and breed != '' and disposition == [] and availability == '':
                response = table.scan(
                    FilterExpression=Attr('animal').eq(animal) & Attr('breed').eq(breed)
                )
            elif animal != '' and breed == '' and disposition != [] and availability != '':
                response = table.scan(
                    FilterExpression=Attr('animal').eq(animal) & Attr('disposition').eq(disposition) & Attr('availability').eq(availability)
                )
            elif animal != '' and breed == '' and disposition != [] and availability == '':
                response = table.scan(
                    FilterExpression=Attr('animal').eq(animal) & Attr('disposition').eq(disposition)
                )
            elif animal != '' and breed == '' and disposition == [] and availability != '':
                response = table.scan(
                    FilterExpression=Attr('animal').eq(animal) & Attr('availability').eq(availability)
                )
            elif animal != '' and breed == '' and disposition == [] and availability == '':
                response = table.scan(
                    FilterExpression=Attr('animal').eq(animal)
                )
            elif animal == '' and breed != '' and disposition != [] and availability != '':
                response = table.scan(
                    FilterExpression=Attr('breed').eq(breed) & Attr('disposition').eq(disposition) & Attr('availability').eq(availability)
                )
            elif animal == '' and breed != '' and disposition != [] and availability == '':
                response = table.scan(
                    FilterExpression=Attr('breed').eq(breed) & Attr('disposition').eq(disposition)
                )
            elif animal == '' and breed != '' and disposition == [] and availability != '':
                response = table.scan(
                    FilterExpression=Attr('breed').eq(breed) & Attr('availability').eq(availability)
                )
            elif animal == '' and breed != '' and disposition == [] and availability == '':
                response = table.scan(
                    FilterExpression=Attr('breed').eq(breed)
                )
            elif animal == '' and breed == '' and disposition != [] and availability != '':
                response = table.scan(
                    FilterExpression=Attr('disposition').eq(disposition) & Attr('availability').eq(availability)
                )
            elif animal == '' and breed == '' and disposition != [] and availability == '':
                response = table.scan(
                    FilterExpression=Attr('disposition').eq(disposition)
                )
            elif animal == '' and breed == '' and disposition == [] and availability != '':
                response = table.scan(
                    FilterExpression=Attr('availability').eq(availability)
                )
            # if not in session, render animals.j2 with data from table "animals"
            if 'id' not in session: 
                return render_template('animals.j2', data=response['Items'])
            # if in session, render loggedanimals.j2 with data from table "animals" if not in session as "admin"
            elif session['id'] != 'admin':
                return render_template('loggedanimals.j2', data=response['Items'])
            # if in session as "admin", render adminanimals.j2 with data from table "animals"
            else:
                return render_template('adminanimals.j2', data=response['Items'])
        # if form is "show_all", redirect to animals page
        elif request.form.get('show_all'):
            return redirect('/animals')

# route for edit with POST method
# POST: only allow if in session as "admin"
# POST: render edit.j2 with data from dynamodb table "animals" where animal_id = <animal_id> from form
@app.route('/edit', methods=['POST'])
def edit():
    # get table "animals" from dynamodb
    table = dynamodb.Table('animals')
    # if "id" in session as "admin"
    if session['id'] == 'admin':
        # get "animal_id" from form
        animal_id = int(request.form['animal_id'])
        # get all items from table "animals" where animal_id = <animal_id>
        response = table.query(
            KeyConditionExpression=Key('animal_id').eq(animal_id)
        )
        # render edit.j2 with data from table "animals"
        return render_template('edit.j2', data=response['Items'])
    # if "id" not in session as "admin"
    else:
        # redirect to animals page
        return redirect('/animals')

# route for update with POST method
# POST: only allow if in session as "admin"
# POST: redirect to /animals if user submits: "animal_id", "image", "animal", "breed", "disposition[]", "create_date", and "availability" for dynamodb table "animals"
# POST: redirect to /animals if user submits: "animal_id" not found in dynamodb table "animals"
@app.route('/update', methods=['POST'])
def update():
    # get table "animals" from dynamodb
    table = dynamodb.Table('animals')
    # if "id" in session as "admin"
    if session['id'] == 'admin':
        # get "animal_id", "image", "animal", "breed", "disposition[]", "create_date", and "availability" from form
        animal_id = int(request.form['animal_id'])
        image = request.form['image']
        animal = request.form['animal']
        breed = request.form['breed']
        disposition = request.form.getlist('disposition[]')
        create_date = request.form['create_date']
        availability = request.form['availability']
        # get all items from table "animals" where animal_id = <animal_id>
        response = table.query(
            KeyConditionExpression=Key('animal_id').eq(animal_id)
        )
        # if "animal_id" found in table "animals"
        if response['Items'] != []:
            # update item in table "animals"
            table.update_item(
                Key={
                    'animal_id': animal_id
                },
                UpdateExpression="set image=:i, animal=:a, breed=:b, disposition=:d, create_date=:c, availability=:av",
                ExpressionAttributeValues={
                    ':i': image,
                    ':a': animal,
                    ':b': breed,
                    ':d': disposition,
                    ':c': create_date,
                    ':av': availability
                },
                ReturnValues="UPDATED_NEW"
            )
            # if availability is "Not Available" or "Available", set pending to "admin" and adopted to "admin"
            if availability == "Not Available" or availability == "Available":
                table.update_item(
                    Key={
                        'animal_id': animal_id
                    },
                    UpdateExpression="set pending=:p, adopted=:ad",
                    ExpressionAttributeValues={
                        ':p': "admin",
                        ':ad': "admin"
                    },
                    ReturnValues="UPDATED_NEW"
                )
            # if availability is "Pending", set adopted to "admin"
            elif availability == "Pending":
                table.update_item(
                    Key={
                        'animal_id': animal_id
                    },
                    UpdateExpression="set adopted=:ad",
                    ExpressionAttributeValues={
                        ':ad': "admin"
                    },
                    ReturnValues="UPDATED_NEW"
                )
            # if availability is "Adopted", set pending to "admin"
            elif availability == "Adopted":
                table.update_item(
                    Key={
                        'animal_id': animal_id
                    },
                    UpdateExpression="set pending=:p",
                    ExpressionAttributeValues={
                        ':p': "admin"
                    },
                    ReturnValues="UPDATED_NEW"
                )
            # redirect to /animals
            return redirect('/animals')
        # if "animal_id" not found in table "animals"
        else:
            # redirect to /animals
            return redirect('/animals')
    # if "id" not in session as "admin"
    else:
        # redirect to /animals
        return redirect('/animals')

# route for /validate with POST method
# POST: only allow if in session as "admin"
# POST: update dynamodb table "animals" where "animal_id" = <animal_id> if "availability" is "Pending"
# POST: update dynamodb table "animals" attribute "availability" to "Adopted"
# POST: update dynamodb table "animals" attribute "adopted" to value of attribute "pending"
# POST: update dynamodb table "animals" attribute "pending" to "admin"
# POST: redirect to /animals
@app.route('/validate', methods=['POST'])
def validate():
    # get animal_id from form
    animal_id = request.form['animal_id']
    # get table "animals" from dynamodb
    table = dynamodb.Table('animals')
    # if "id" in session as "admin"
    if session['id'] == 'admin':
        # get all items from table "animals" where animal_id = <animal_id>
        response = table.query(
            KeyConditionExpression=Key('animal_id').eq(int(animal_id))
        )
        # if "availability" is "Pending"
        if response['Items'][0]['availability'] == 'Pending':
            # update item in table "animals" where animal_id = <animal_id>
            table.update_item(
                Key={
                    'animal_id': int(animal_id)
                },
                # update "availability" to "Adopted"
                # update "adopted" to value of "pending"
                # update "pending" to "admin"
                UpdateExpression="set availability=:a, adopted=:ad, pending=:p",
                ExpressionAttributeValues={
                    ':a': 'Adopted',
                    ':ad': response['Items'][0]['pending'],
                    ':p': 'admin'
                },
                ReturnValues="UPDATED_NEW"
            )
            # redirect to /animals
            return redirect('/animals')
        # if "availability" is not "Pending"
        else:
            # redirect to /animals
            return redirect('/animals')
    # if "id" not in session as "admin"
    else:
        # redirect to /animals
        return redirect('/animals')

# route for /relinquish with POST method
# POST: only allow if in session as owner of animal
# POST: update dynamodb table "animals" where "animal_id" = <animal_id> if "availability" is "Pending" or "Adopted"
# POST: update dynamodb table "animals" attribute "pending" to "admin"
# POST: update dynamodb table "animals" attribute "adopted" to "admin"
# POST: redirect to /profile
@app.route('/relinquish', methods=['POST'])
def relinquish():
    # get animal_id from form
    animal_id = request.form['animal_id']
    # get table "animals" from dynamodb
    table = dynamodb.Table('animals')
    # if "id" in session
    if 'id' in session:
        # get all items from table "animals" where animal_id = <animal_id>
        response = table.query(
            KeyConditionExpression=Key('animal_id').eq(int(animal_id))
        )
        # check if "id" in session is the owner of the animal
        if session['id'] == response['Items'][0]['pending'] or session['id'] == response['Items'][0]['adopted']:
            # update item in table "animals" where animal_id = <animal_id>
            table.update_item(
                Key={
                    'animal_id': int(animal_id)
                },
                # update "availability" to "Available"
                # update "pending" to "admin"
                # update "adopted" to "admin"
                UpdateExpression="set availability=:a, pending=:p, adopted=:ad",
                ExpressionAttributeValues={
                    ':a': 'Available',
                    ':p': 'admin',
                    ':ad': 'admin'
                },
                ReturnValues="UPDATED_NEW"
            )
            # redirect to /profile
            return redirect('/profile')
        # if "availability" is not "Pending" or "Adopted"
        else:
            # redirect to /profile
            return redirect('/profile')
    # if "id" not in session
    else:
        # redirect to /profile
        return redirect('/profile')

# route for adopt with POST method
# POST: only allow if in session and not as "admin"
# POST: update dynamodb table "animals" where "animal_id" = <animal_id> if "availability" is "Available"
# POST: update dynamodb table "animals" attribute "pending" to session id
# POST: redirect to /profile
@app.route('/adopt', methods=['POST'])
def adopt():
    # get animal_id from form
    animal_id = request.form['animal_id']
    # get table "animals" from dynamodb
    table = dynamodb.Table('animals')
    # if "id" in session and not as "admin"
    if 'id' in session and session['id'] != 'admin':
        # get all items from table "animals" where animal_id = <animal_id>
        response = table.query(
            KeyConditionExpression=Key('animal_id').eq(int(animal_id))
        )
        # if "availability" is "Available"
        if response['Items'][0]['availability'] == 'Available':
            # update item in table "animals" where animal_id = <animal_id>
            table.update_item(
                Key={
                    'animal_id': int(animal_id)
                },
                # update "availability" to "Pending"
                # update "pending" to session id
                UpdateExpression="set availability=:a, pending=:p",
                ExpressionAttributeValues={
                    ':a': 'Pending',
                    ':p': session['id']
                },
                ReturnValues="UPDATED_NEW"
            )
            # redirect to /profile
            return redirect('/profile')
        # if "availability" is not "Available"
        else:
            # redirect to /animals
            return redirect('/animals')
    # if "id" not in session and not as "admin"
    else:
        # redirect to /animals
        return redirect('/animals')

# route for delete/<id> with POST method
# delete from dynamodb table "users" where id = <id>
# redirect to /logout
@app.route('/delete/<id>', methods=['POST'])
def delete(id):
    # get table "users" from dynamodb
    table = dynamodb.Table('users')
    # delete from table "users" where id = <id>
    table.delete_item(
        Key={
            'id': id
        }
    )
    # redirect to /logout
    return redirect('/logout')

# route for animals/<animal_id> deletion with POST method
# POST: delete from dynamodb table "animals" where animal_id = <animal_id> if in session as admin
# POST: redirect to /animals
@app.route('/animals/<animal_id>', methods=['POST'])
def delete_animal(animal_id):
    # get table "animals" from dynamodb
    table = dynamodb.Table('animals')
    # if "id" in session as "admin"
    if session['id'] == 'admin':
        # convert animal_id to an integer
        animal_id = int(animal_id)
        # delete from table "animals" where animal_id = <animal_id>
        table.delete_item(
            Key={
                'animal_id': animal_id
            }
        )
        # redirect to /animals
        return redirect('/animals')
    # if "id" not in session as "admin"
    else:
        # redirect to /animals
        return redirect('/animals')

# host in debug mode at 0.0.0.0 on port 5000
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
