"""Server for movie ratings app."""

from flask import Flask
from flask import (Flask, render_template, request,
                   flash, session, redirect, jsonify)
from Model import connect_to_db, db
import crud
from datetime import datetime
from jinja2 import StrictUndefined
import requests
import os
import json

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
        return jsonify({'success': False, 'message': 'The email or password you entered was incorrect.'})
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

            webtoons = crud.create_UserList('Webtoons', user_id)
            books = crud.create_UserList('Books', user_id)
            tvshows = crud.create_UserList('TV Shows', user_id)
            movies = crud.create_UserList('Movies', user_id)
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
    if "list_id" in session:
        del session["list_id"]

    user = crud.get_user_by_id(user_id)
    fname = user.fname
    lists = crud.get_all_user_list_by_user_id(user_id)

    return render_template('profile.html', fname=fname, lists=lists)


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
    # Find the media via API AND media table to see if the media has been
    # If nothing returns
    media = crud.create_media(type, name, category, summary)
    db.session.add(media)
    db.session.commit()

    if (name == None) or (type == None) or (category == None) or (summary == None) or (rating == None) or (thoughts == None) or (recommend_or_not == None):
        return jsonify({'success': False, 'message': "Please fill out all boxes!"})
    else:
        now = datetime.now()
        current_time = now.strftime("%m-%d-%Y")
        created_at = current_time
        form = crud.create_form(media, user, rating,
                                thoughts, recommend_or_not, created_at)
        db.session.add(form)
        db.session.commit()

        if type.lower() == 'webtoon':
            user_list = crud.get_list_by_name_and_user_id('Webtoons', user_id)
            form_map = crud.create_FormMap(user_list.userlist_id, form.form_id)
            db.session.add(form_map)
            db.session.commit()

        if type.lower() == 'book':
            user_list = crud.get_list_by_name_and_user_id('Books', user_id)
            form_map = crud.create_FormMap(user_list.userlist_id, form.form_id)
            db.session.add(form_map)
            db.session.commit()
        if type.lower() == 'tvshow':
            user_list = crud.get_list_by_name_and_user_id('TV Shows', user_id)
            form_map = crud.create_FormMap(user_list.userlist_id, form.form_id)
            db.session.add(form_map)
            db.session.commit()
        if type.lower() == 'movie':
            user_list = crud.get_list_by_name_and_user_id('Movies', user_id)
            form_map = crud.create_FormMap(user_list.userlist_id, form.form_id)
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
    name = request.json.get("name")

    if (name == None):
        return jsonify({'success': False, 'message': "Please fill out all boxes!"})
    else:
        list = crud.create_UserList(name, user_id)
        db.session.add(list)
        db.session.commit()
        session['list_id'] = list.userlist_id

        return jsonify({'success': True, 'message': "List Created!"})


@app.route('/addFormToList', methods=['POST'])
def add_form_to_list():
    if 'list_id' in session:
        current_list_id = session['list_id']
    else:
        return jsonify({'success': False, 'message': "Please Create A New List First!"})

    # Get List_id from the API request
    list = crud.get_list_by_id(current_list_id)
    # Get form_id from the API request
    form_id = request.json.get("selectedFormId")
    # Create a form map for the selected form and the created list
    form_map = crud.create_FormMap(list.userlist_id, form_id)
    db.session.add(form_map)
    db.session.commit()

    return jsonify({'success': True})


@app.route('/viewLists/<list_id>', methods=['GET'])
def view_users_lists(list_id):
    """Allows user to view their premade or unique lists."""
    user_id = session["user_id"]
    current_list = crud.get_list_by_id(list_id)
    # current_list = crud.get_list_by_name_and_user_id(name, user_id)
    form_maps = crud.get_form_map_by_list_id(current_list.userlist_id)
    all_forms = []
    for form_map in form_maps:
        form = crud.get_form_from_form_id(form_map.form_id)
        all_forms.append(form)
    full_forms = []
    for form in all_forms:
        media_and_form = {}
        media_id = form.media_id
        media = crud.get_media_by_id(media_id)
        media_and_form['form'] = form
        media_and_form['media'] = media
        full_forms.append(media_and_form)

    return render_template('viewList.html', name=current_list.name, full_forms=full_forms)


@app.route('/api/suggestions')
def get_suggestions():
    query = request.args.get('query')
    media_type = request.args.get('type')
    results = []

    if media_type == 'movie':
        # Make a request to the TMDb API to search for movies and TV shows
        tmdb_api_key = '34e6115227f3afeb13733d2f8978dae9'
        url = f'https://api.themoviedb.org/3/search/multi?api_key={tmdb_api_key}&query={query}'
        response = requests.get(url)
        data = response.json()

        for result in data['results']:
            if result['media_type'] == 'movie':
                summary = result['overview']
                title = ""
                if 'title' in result:
                    title = result['title']
                elif 'name' in result:
                    title = result['name']
                movie_id = result['id']

                new_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={tmdb_api_key}"
                new_response = requests.get(new_url)
                genres = new_response.json().get('genres', [])
                genre = ""
                if genres:
                    genre = genres[0]['name']

                results.append(
                    {'category': genre, 'summary': summary, 'title': title})
            else:
                continue

        # Return the list of suggestions as a JSON response
        return jsonify(results)
    elif media_type == 'tvshow':
        tmdb_api_key = '34e6115227f3afeb13733d2f8978dae9'
        url = f'https://api.themoviedb.org/3/search/multi?api_key={tmdb_api_key}&query={query}'
        response = requests.get(url)
        data = response.json()

        for result in data['results']:
            if result['media_type'] == 'tv':
                category = 'TV Show'
                summary = result['overview']
                title = ""
                if 'title' in result:
                    title = result['title']
                elif 'name' in result:
                    title = result['name']
                movie_id = result['id']

                new_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={tmdb_api_key}"
                new_response = requests.get(new_url)
                genres = new_response.json().get('genres', [])
                genre = ""
                if genres:
                    genre = genres[0]['name']

                results.append(
                    {'category': genre, 'summary': summary, 'title': title})
            else:
                continue
        return jsonify(results)
    elif media_type == 'book':
        url = f"http://openlibrary.org/search.json?q={query}"
        response = requests.get(url)

        # Check if the request was successful (i.e. status code 200)
        if response.status_code == 200:
            # Parse the response JSON and extract the list of search results
            data = response.json()
            search_results = data["docs"]

            # Print the title and author of each search result
            for result in search_results:
                # print('RESULT')
                # print(result)
                book_id = result["seed"][0].replace("/books/", "")

                # print('BOOKID')
                # print(book_id)

                # Send a GET request to the Open Library API for the book summary
                summary_url = f"http://openlibrary.org/api/books?bibkeys=OLID:{book_id}&format=json&jscmd=details"
                # print(summary_url)
                summary_response = requests.get(summary_url)
                summary_data = summary_response.json()
                # print('SUMMARY DATA!!!!')
                # print(summary_data)
                # print(summary_data[f"OLID:{book_id}"]["details"])
                # summary = summary_data[f"OLID:{book_id}"]["details"]["description"]
                # print('rESULT!!!')
                # print(summary)
                title = result["title"]
                author = result.get("author_name", ["Unknown"])[0]
                # print('SUMMARY!')
                # print(summary)
                # print(f"{title} by {author}")
                category = ''
                results.append(
                    {'category': category, 'summary': "", 'title': f"{title} by {author}"})
        else:
            print(f"Error: {response.status_code} - {response.reason}")

        return jsonify(results)

    elif media_type == 'webtoon':
        # with open('updated_example.json', encoding="utf-8") as f:
        #     data = json.load(f)

        # print(data)

        # book_title = data[0]["title"]
        # results.append(
        #     {'category': category, 'summary': '', 'title': book_title})

        return jsonify(results)

    return jsonify(results)


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
