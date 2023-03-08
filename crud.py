"""CRUD operations."""

from Model import db, User, UserList, ListMedia, Form, Media, connect_to_db

def create_user(fname, lname, email, password):
    """Create and return a new user."""

    user = User(fname=fname,
                lname=lname, 
                email=email, 
                password=password)

    return user

def get_user_by_email(email):
    """Returns a user by email."""

    return User.query.filter(User.email == email).first()

def get_user_password(password):
    """Returns user's password."""

    return User.query.filter(User.password == password).first()


def create_UserList(name, user):
    """Create and return a User's List."""

    userlist = UserList(name=name,
                        user=user)
    
    return userlist

def create_ListMedia(userlist, form):
    """Create and return Media for a list."""

    listmedia = ListMedia(userlist=userlist,
                        form=form)
    
    return listmedia

def create_form(media, user, rating, thoughts, recommend_or_not, created_at):
    """Create and return a form."""

    form = Form(media=media,
                user=user,
                rating=rating,
                thoughts=thoughts,
                recommend_or_not=recommend_or_not,
                created_at=created_at)
    
    return form

def create_media(type, name, category, summary):
    """Create and return a specific media."""

    media = Media(type=type,
                name=name,
                category=category,
                summary=summary)
    
    return media

# def create_MediaType(type):
#     """Create and return a media's type"""

#     mediatype = MediaType(type=type)

#     return mediatype



if __name__ == '__main__':
    from server import app
    connect_to_db(app)