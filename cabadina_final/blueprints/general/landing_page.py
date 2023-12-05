from flask import Blueprint, render_template, session

landing_page_bp = Blueprint('landing_page', __name__, template_folder='templates')

@landing_page_bp.route('/')
def landing_page():
  return render_template(
    'pages/general/landing_page.html',
    logged_in=session.get('logged_in', False),
    as_user=session.get('as_user', False)
  )