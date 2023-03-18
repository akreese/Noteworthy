"""CRUD operations."""

from Model import db, User, UserList, FormMap, Form, Media, connect_to_db

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


def get_user_by_id(user_id):
    """Returns a user by ID."""

    return User.query.filter(User.user_id == user_id).first()


def get_user_password(password):
    """Returns user's password."""

    return User.query.filter(User.password == password).first()


def get_user_list_by_user_id(user_id):
    """Returns a user's list by their ID."""

    return UserList.query.filter(UserList.user_id == user_id).first()


def create_UserList(name, user_id):
    """Create and return a User's List."""

    userlist = UserList(name=name,
                        user_id=user_id)
    
    return userlist

def create_FormMap(userlist_id, form_id):
    """Create and return Media for a list."""

    formMap = FormMap(userlist_id=userlist_id,
                        form_id=form_id)
    
    return formMap

def create_form(media_id, user_id, rating, thoughts, recommend_or_not, created_at):
    """Create and return a form."""

    form = Form(media_id=media_id,
                user_id=user_id,
                rating=rating,
                thoughts=thoughts,
                recommend_or_not=recommend_or_not,
                created_at=created_at)
    
    return form


def get_forms_by_user_id(user_id):
    """Return all forms filled out by user."""

    return Form.query.filter(Form.user_id == user_id).all()

def get_media_from_forms(media_id):
    """Return media id from the pulled form."""

    return Form.query.filter(Form.media_id == media_id).first()

def create_media(type, name, category, summary):
    """Create and return a specific media."""

    media = Media(type=type,
                name=name,
                category=category,
                summary=summary)
    
    return media

def get_media_by_id(media_id):
    """Returns media id for that media."""

    return Media.query.filter(Media.media_id == media_id).first()


if __name__ == '__main__':
    from server import app
    connect_to_db(app)