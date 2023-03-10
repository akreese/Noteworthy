"""Server for movie ratings app."""

from flask import Flask
from flask import (Flask, render_template, request, flash, session, redirect, jsonify)
from Model import connect_to_db, db
import crud
from jinja2 import StrictUndefined


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """View homepage and login box."""

    return render_template('homepage.html')




@app.route('/api/validateUser', methods=['GET'])
def validate_user():
    """Validate User input from login submission."""
    request_email = request.args.get("email")
    request_password = request.args.get("password")

    user = crud.get_user_by_email(request_email) 

    if not user or user.password != request_password:
        return jsonify({'success': False, 'message':'The email or password you entered was incorrect.'})
    else:
        return jsonify({'success': True,
                    'email': user.email,
                    'password': user.password})




@app.route('/createprofile', methods=['GET'])
def new_user():
    """Create new user."""

    # fname = request.form.get("fname")
    # lname = request.form.get("lname")
    # email = request.form.get("email")
    # password = request.form.get("password")

    # user = crud.get_user_by_email(email)

    # if user:
    #     flash("Email already in use. Please use another one.")
    # else:
    #     user = crud.create_user(fname, lname, email, password)
    #     db.session.add(user)
    #     db.session.commit()
    #     flash("Account Created!")

    #     return redirect("/profile/<user_id>")

    return render_template('newuser.html')

@app.route('/api/createUser', methods=['POST'])
def create_user():
    print('CREATE USER CALLED')
    print(request.data)
    return jsonify({'success': False, 'message':'The email or password you entered was incorrect.'})

    # fname = request.form.get("fname")
    # lname = request.form.get("lname")
    # email = request.form.get("email")
    # password = request.form.get("password")

    # user = crud.get_user_by_email(email)

    # if user:
    #     flash("Email already in use. Please use another one.")
    # else:
    #     user = crud.create_user(fname, lname, email, password)
    #     db.session.add(user)
    #     db.session.commit()
    #     flash("Account Created!")

    #     return redirect("/profile/<user_id>")
    # """See if email has already been used."""
    # request_email = request.args.get("email")

    # user = crud.get_user_by_email(request_email) 

    # if user:
    #     return jsonify({'success': False, 'message': "12"})
    # else:
    #     return jsonify({'success': True,
    #                 'email': user.email,
    #                 'password': user.password})

@app.route('/profile')
def user_profile():
    """View User's profile"""

    return render_template('profile.html')





if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)