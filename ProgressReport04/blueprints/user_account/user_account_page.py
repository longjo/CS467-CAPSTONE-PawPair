from flask import Blueprint, redirect, render_template, session

user_account_page_bp = Blueprint('user_account', __name__, template_folder='templates')

@user_account_page_bp.route('/user_account')
def user_account():
    if session.get('logged_in'):
        name = f"{session['first_name']} {session['last_name']}"
        email = session['email']

        # Display the user's information on the page.
        return render_template(
            'pages/user_account/user_account_page.html',
            logged_in=session.get('logged_in', False),
            as_user=session.get('as_user', False),
            name=name,
            email=email
        )
    else:
        return redirect('/user_login')