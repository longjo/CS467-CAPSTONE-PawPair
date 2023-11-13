# Import all relevant blueprints before registering in app.py

from .user_login_page import user_login_page_bp
from .user_signup_page import user_signup_page_bp

from .shelter_login_page import shelter_login_page_bp
from .shelter_signup_page import shelter_signup_page_bp

from .logout_page import logout_page_bp
