from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

#11.24 logins
from flask import abort
from flask import session

import qrcode
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pets.db'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database models (User and Pet)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    contact_number = db.Column(db.String(15), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    # Add additional fields as needed

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    species = db.Column(db.String(50), nullable=False)
    breed = db.Column(db.String(100), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), default="available")


    #11.20.23 additions--beg
    disposition = db.Column(db.String(255))  # New field
    availability = db.Column(db.String(50))  # New field
    news_item = db.Column(db.Text)  # New field
    #11.20.23 additions--end


    picture_url = db.Column(db.String(255), nullable=True)
    # Add additional fields as needed

@app.route('/')
def home():
    return render_template('home.html')

# Add additional routes here
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         email = request.form['email']
#         password = request.form['password']
#         contact_number = request.form['contact_number']
#         hashed_password = generate_password_hash(password)
#         is_admin = 'is_admin' in request.form

#         new_user = User(username=username, email=email, password=hashed_password, 
#                         contact_number=contact_number, is_admin=is_admin)
#         db.session.add(new_user)
#         db.session.commit()

#         return redirect(url_for('login'))
#     return render_template('register.html')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        contact_number = request.form['contact_number']
        hashed_password = generate_password_hash(password)
        is_admin = 'is_admin' in request.form

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return 'Email already in use'  # Or redirect to a different page with a message

        new_user = User(username=username, email=email, password=hashed_password,
                        contact_number=contact_number, is_admin=is_admin)
        db.session.add(new_user)
        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            return 'Registration failed due to a database error'

        return redirect(url_for('login'))
    return render_template('register.html')



from werkzeug.security import check_password_hash
from flask import session


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['username'] = user.username
            session['is_admin'] = user.is_admin  # Store admin status in session
            return redirect(url_for('home'))
        else:
            return 'Invalid username or password'  # Implement better error handling

    return render_template('login.html')




# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         user = User.query.filter_by(username=username).first()
#         if user and check_password_hash(user.password, password):
#             session['username'] = user.username
#             return redirect(url_for('home'))  # Redirect to home or user dashboard after login
#         else:
#             return 'Invalid username or password'  # Implement better error handling

#     return render_template('login.html')

@app.route('/users')
def show_users():
    users = User.query.all()  # Fetch all users from the database
    return render_template('users.html', users=users)


# @app.route('/add_pet', methods=['GET', 'POST'])
# def add_pet():
#     if request.method == 'POST':
#         name = request.form['name']
#         species = request.form['species']
#         breed = request.form['breed']
#         age = request.form['age']
#         description = request.form['description']
#         picture = request.files['picture']

#         filename = secure_filename(picture.filename)
#         picture_path = os.path.join('static/images', filename)
#         picture.save(picture_path)

#         new_pet = Pet(name=name, species=species, breed=breed, age=age, description=description, picture_url=picture_path)
#         db.session.add(new_pet)
#         db.session.commit()

#         return redirect(url_for('home'))
#     return render_template('add_pet.html')


@app.route('/add_pet', methods=['GET', 'POST'])
def add_pet():
            
    if 'username' in session and session.get('is_admin', False):







            if request.method == 'POST':
                name = request.form['name']
                species = request.form['species']
                breed = request.form['breed']
                age = request.form['age']
                description = request.form['description']
                picture = request.files['picture']

                filename = secure_filename(picture.filename)
                picture_path = os.path.join('images', filename)  # Modified line
                picture.save(os.path.join('static/images', filename))  # Modified line


                #11.20.23 additons--beg
                dispositions = request.form.getlist('disposition')
                disposition_string = ', '.join(dispositions)  # Combine into a single string

                availability = request.form.get('availability')
                news_item = request.form.get('news_item')
                
                new_pet = Pet(name=name, species=species, breed=breed, age=age, 
                            description=description, picture_url=picture_path, 
                            disposition=disposition_string, availability=availability, 
                            news_item=news_item)
                
                #11.20.23 additions-end

                #new_pet = Pet(name=name, species=species, breed=breed, age=age, description=description, picture_url=picture_path)
                
                
                
                db.session.add(new_pet)
                db.session.commit()

                return redirect(url_for('home'))
            return render_template('add_pet.html')
    

    else:
        # Show an intermediate page before redirecting to home
        return render_template('not_authorized.html')



# @app.route('/pets')
# def show_pets():
#     pets = Pet.query.all()  # Fetch all pets from the database
#     return render_template('pets.html', pets=pets)

@app.route('/pets')
def show_pets():
    page = request.args.get('page', 1, type=int)
    per_page = 6  # Number of pets per page
    pets = Pet.query.paginate(page, per_page, False)
    next_url = url_for('show_pets', page=pets.next_num) if pets.has_next else None
    prev_url = url_for('show_pets', page=pets.prev_num) if pets.has_prev else None
    return render_template('pets.html', pets=pets.items, next_url=next_url, prev_url=prev_url)

@app.route('/pet/<int:pet_id>')
def pet_profile(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    return render_template('pet_profile.html', pet=pet)


@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    return redirect(url_for('home'))



# @app.route('/search', methods=['GET', 'POST'])
# def search():
#     if request.method == 'POST':
#         species = request.form.get('species')
#         breed = request.form.get('breed')
#         disposition = request.form.getlist('disposition')

#         # Construct the query based on the search parameters
#         query = Pet.query
#         if species:
#             query = query.filter(Pet.species.ilike(f"%{species}%"))
#         if breed:
#             query = query.filter(Pet.breed.ilike(f"%{breed}%"))
#         if disposition:
#             query = query.filter(Pet.disposition.in_(disposition))

#         pets = query.all()
#         return render_template('search_results.html', pets=pets)

#     return render_template('search.html')
@app.route('/search', methods=['GET', 'POST'])
def search():
    # Lists of common breeds for dogs and cats
    dog_breeds = ["Labrador", "German Shepherd", "Golden Retriever", "Bulldog", "Beagle", "Other"]
    cat_breeds = ["Siamese", "Persian", "Maine Coon", "Ragdoll", "Bengal", "Other"]

    if request.method == 'POST':
        species = request.form.get('species')
        breed = request.form.get('breed')
        disposition = request.form.getlist('disposition')

        # Construct the query based on the search parameters
        query = Pet.query
        if species:
            query = query.filter(Pet.species.ilike(f"%{species}%"))
        if breed and breed != "All":
            query = query.filter(Pet.breed.ilike(f"%{breed}%"))
        if disposition:
            # You'll need to adjust this part based on how you store disposition data
            for dispo in disposition:
                query = query.filter(Pet.disposition.ilike(f"%{dispo}%"))

        pets = query.all()
        return render_template('search_results.html', pets=pets)

    return render_template('search.html', dog_breeds=dog_breeds, cat_breeds=cat_breeds)


@app.route('/admin')
def admin():
    # You might want to add access control here later
    return render_template('admin.html')


@app.route('/debug_pictures')
def debug_pictures():
    pets = Pet.query.all()
    for pet in pets:
        print(pet.name, pet.picture_url)
    return "Check the console for picture URLs."



# @app.route('/adopt_pet/<int:pet_id>', methods=['POST'])
# def adopt_pet(pet_id):
#     if 'username' not in session:
#         return redirect(url_for('login'))

#     pet = Pet.query.get_or_404(pet_id)
#     if pet.availability.lower() == 'available':
#         pet.availability = 'Adopted'
#         db.session.commit()
#         return redirect(url_for('pet_profile', pet_id=pet_id))
#     else:
#         return "This pet is not available for adoption.", 400



@app.route('/adopt_pet/<int:pet_id>', methods=['POST'])
def adopt_pet(pet_id):
    if 'username' not in session:
        return redirect(url_for('login'))

    pet = Pet.query.get_or_404(pet_id)
    if pet.availability.lower() == 'available':
        pet.availability = 'Adopted'
        
        # Generate a unique confirmation number
        confirmation_number = f"ADOPT-{pet_id}-{os.urandom(4).hex()}"

        # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(confirmation_number)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Save QR code image
        qr_code_file = f"qr_codes/qr_{confirmation_number}.png"
        img.save(os.path.join('static', qr_code_file))

        db.session.commit()

        # Render the confirmation page
        return render_template('confirmation.html', confirmation_number=confirmation_number, qr_code_file=qr_code_file)
    else:
        return "This pet is not available for adoption.", 400









if __name__ == '__main__':
    app.run(debug=True)
