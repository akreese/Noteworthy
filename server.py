"""Server for movie ratings app."""

from flask import Flask
from flask import (Flask, render_template, request, flash, session, redirect, jsonify)
from Model import connect_to_db, db
import crud
from datetime import datetime
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
        session['user_id'] = user.user_id
        return jsonify({'success': True,
                    'email': user.email,
                    'password': user.password})




@app.route('/createprofile', methods=['GET'])
def new_user():
    """Create new user."""

    return render_template('newuser.html')



@app.route('/api/createUser', methods=['POST'])
def create_user():
    """Add new user to database."""
    fname = request.json.get("fname")
    lname = request.json.get("lname")
    email = request.json.get("email")
    password = request.json.get("password")
    password_2 = request.json.get("rePassword")
    
    user = crud.get_user_by_email(email)

    if user:
        return jsonify({'success': False, 'message': "Email already in use. Please use another one."})
    else:
        if password != password_2:
            return jsonify({'success': False, 'message': "Passwords do not match. Please double check password."})

        else:
            user = crud.create_user(fname, lname, email, password)
            db.session.add(user)
            db.session.commit()
            user_id = user.user_id 

            webtoons = crud.create_UserList('webtoons',user_id)
            books = crud.create_UserList('books', user_id)
            tvshows = crud.create_UserList('tvshows', user_id)
            movies = crud.create_UserList('movies', user_id)
            db.session.add(webtoons)
            db.session.add(books)
            db.session.add(tvshows)
            db.session.add(movies)
            db.session.commit()
            session['user_id'] = user_id
            return jsonify({'success': True})



@app.route('/profile')
def user_profile():
    """View User's profile"""
    user_id = session["user_id"]
    user = crud.get_user_by_id(user_id)
    fname = user.fname

    lists = crud.get_all_user_list_by_user_id(user_id)
    print('LIST!!!')
    print(lists)
    return render_template('profile.html', fname=fname, lists = lists)



@app.route('/newForm', methods=['GET'])
def new_form():
    """Allow's user to see form."""

    return render_template('form.html')



@app.route('/createForm', methods=['POST'])
def create_form():
    """Allows user to create a new form for media completion"""
    user_id = session["user_id"]
    user = crud.get_user_by_id(user_id)

    name = request.json.get("name")
    type = request.json.get("mediaType")
    category = request.json.get("category")
    summary = request.json.get("summary")
    rating = request.json.get("rating")
    thoughts = request.json.get("thoughts")
    recommend_or_not = request.json.get("recommend")
    #Find the media via API AND media table to see if the media has been
    #If nothing returns
    media = crud.create_media(type,name,category,summary)
    db.session.add(media)
    db.session.commit()

    if (name == None) or (type == None) or (category == None) or (summary == None) or (rating == None) or (thoughts == None) or (recommend_or_not == None):
        return jsonify({'success': False, 'message': "Please fill out all boxes!"})
    else:
        now = datetime.now()
        current_time = now.strftime("%m-%d-%Y")
        created_at = current_time
        form = crud.create_form(media, user, rating, thoughts, recommend_or_not, created_at)
        db.session.add(form)
        db.session.commit()

        if type.lower() == 'webtoon':
            user_list = crud.get_list_by_name_and_user_id('webtoons',user_id)
            form_map = crud.create_FormMap(user_list.userList_id,form.form_id)
            db.session.add(form_map)
            db.session.commit()

        if type.lower() == 'book':
            user_list = crud.get_list_by_name_and_user_id('books',user_id)
            form_map = crud.create_FormMap(user_list.userList_id,form.form_id)
            db.session.add(form_map)
            db.session.commit()
        if type.lower() == 'tvshow':
            user_list = crud.get_list_by_name_and_user_id('tvshows',user_id)
            form_map = crud.create_FormMap(user_list.userList_id,form.form_id)
            db.session.add(form_map)
            db.session.commit()
        if type.lower() == 'movie':
            user_list = crud.get_list_by_name_and_user_id('movies',user_id)
            form_map = crud.create_FormMap(user_list.userList_id,form.form_id)
            db.session.add(form_map)
            db.session.commit()


        return jsonify({'success': True})



@app.route('/newList', methods=['GET'])
def new_list():
    """Allows user to create a new list."""
    user_id = session["user_id"]
    forms = crud.get_forms_by_user_id(user_id)
    full_forms = []
    for form in forms:
        media_and_form = {}
        media_id = form.media_id
        media = crud.get_media_by_id(media_id)
        media_and_form['form'] = form
        media_and_form['media'] = media
        full_forms.append(media_and_form)
    return render_template('createList.html', forms=forms, full_forms=full_forms)

@app.route('/createList', methods=['POST'])
def create_list():
    """Allows user to create a new list."""
    user_id = session["user_id"]
    user = crud.get_user_by_id(user_id)
    return None


@app.route('/viewLists')
def view_users_lists():
    """Allows user to view their premade or unique lists."""
    user_id = session["user_id"]
    user = crud.get_user_by_id(user_id)
    fname = user.fname

    return render_template('viewLists', fname=fname )

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)