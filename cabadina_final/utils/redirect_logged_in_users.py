from flask import redirect, session

def redirect_logged_in_users():
    # Send logged in users to the appropriate account page

    logged_in=session.get('logged_in', False)
    as_user=session.get('as_user', False)
    print(logged_in)
    print(as_user)
    if logged_in:
        if as_user:
            return redirect('/user_account')
        else:
            return redirect('/shelter_account')
