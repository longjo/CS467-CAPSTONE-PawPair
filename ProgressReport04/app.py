from flask import Flask

from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE, SECRET_KEY

from blueprints.auth import *
from blueprints.general import *
from blueprints.user_account import *
from blueprints.shelter_account import *
from blueprints.shelter_animals import *

app = Flask(__name__)

# Register authorization blueprints
app.register_blueprint(user_login_page_bp)               # /user_login
app.register_blueprint(user_signup_page_bp)              # /user_signup
app.register_blueprint(shelter_login_page_bp)            # /shelter_login
app.register_blueprint(shelter_signup_page_bp)           # /shelter_signup
app.register_blueprint(logout_page_bp)                   # /logout

# Register general blueprints
app.register_blueprint(db_test_page_bp)                  # /testing
app.register_blueprint(landing_page_bp)                  # /

# Register user account blueprints
app.register_blueprint(user_account_page_bp)             # /user_account
app.register_blueprint(edit_user_name_page_bp)           # /edit_user_name
app.register_blueprint(edit_user_email_page_bp)          # /edit_user_email
app.register_blueprint(change_user_password_page_bp)     # /change_user_password
app.register_blueprint(delete_user_account_page_bp)      # /delete_user_account

# Register shelter account blueprints
app.register_blueprint(shelter_account_page_bp)          # /shelter_account
app.register_blueprint(edit_shelter_name_page_bp)        # /edit_shelter_name
app.register_blueprint(edit_shelter_email_page_bp)       # /edit_shelter_email
app.register_blueprint(edit_shelter_zip_page_bp)         # /edit_shelter_zip
app.register_blueprint(change_shelter_password_page_bp)  # /change_shelter_password
app.register_blueprint(delete_shelter_account_page_bp)   # /delete_shelter_account

# Register shelter animal blueprints
app.register_blueprint(add_shelter_animal_bp)            # /add_shelter_animal
app.register_blueprint(edit_shelter_animal_bp)           # /edit_shelter_animal/<int: animal_id>
app.register_blueprint(delete_shelter_animal_bp)         # /delete_shelter_animal/<int: animal_id>


# Configure the database connection
app.config['MYSQL_HOST'] = MYSQL_HOST
app.config['MYSQL_USER'] = MYSQL_USER
app.config['MYSQL_PASSWORD'] = MYSQL_PASSWORD
app.config['MYSQL_DATABASE'] = MYSQL_DATABASE

# Configure security key with random string
app.config['SECRET_KEY'] = SECRET_KEY

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=5000)