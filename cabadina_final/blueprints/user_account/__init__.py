# Import all relevant blueprints before registering in app.py

from .user_account_page import user_account_page_bp
from .edit_user_name_page import edit_user_name_page_bp
from .edit_user_email_page import edit_user_email_page_bp
from .change_user_password_page import change_user_password_page_bp
from .delete_user_account_page import delete_user_account_page_bp