from flask import Blueprint, redirect, session

logout_page_bp = Blueprint('logout', __name__, template_folder='templates')

@logout_page_bp.route('/logout')
def logout():

    # Clear the current session
    session.clear()

    # Return to homepage
    return redirect('/')