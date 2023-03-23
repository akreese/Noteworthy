"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import Model
import server

os.system("dropdb consumedmedia")
os.system("createdb consumedmedia")

Model.connect_to_db(server.app)
Model.db.create_all()

# Loading media data from JSON file
with open('data/fakemedia.json') as f:
    media_data = json.loads(f.read())

# Creating media to be stored in a list to be used in the database
media_in_db = []
for media in media_data:
    type, name, category, summary = (
        media["type"],
        media["name"],
        media["category"],
        media["summary"]
    )
    db_media = crud.create_media(type, name, category, summary)
    media_in_db.append(db_media)

Model.db.session.add_all(media_in_db)
Model.db.session.commit()

recommend = ["yes", "no"]
# Creating 10 users; each user will create 10 different forms
for n in range(10):
    email = f"user{n}@test.com" 
    fname = "Tester"
    lname = f"{n}"
    password = "test"

    user = crud.create_user(fname, lname, email, password)
    Model.db.session.add(user)
    Model.db.session.commit()
    user_id = user.user_id
    webtoons = crud.create_UserList('Webtoons',user_id)
    books = crud.create_UserList('Books', user_id)
    tvshows = crud.create_UserList('TV Shows', user_id)
    movies = crud.create_UserList('Movies', user_id)
    Model.db.session.add(webtoons)
    Model.db.session.add(books)
    Model.db.session.add(tvshows)
    Model.db.session.add(movies)

    now = datetime.now()
    current_time = now.strftime("%m-%d-%Y")

    for _ in range(10):
        media = choice(media_in_db)
        rating = randint(1,5)
        thoughts = "These are my thoughts"
        recommend_or_not = choice(recommend)
        created_at = current_time

        form = crud.create_form(media, user, rating, thoughts, recommend_or_not, created_at)
        Model.db.session.add(form)

Model.db.session.commit()