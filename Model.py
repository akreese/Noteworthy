"""Models for media consumption app."""
import enum
from sqlalchemy import Enum
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    fname = db.Column(db.String)
    lname = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    forms = db.relationship("Form", back_populates="user")
    userlists = db.relationship("UserList", back_populates="user")

    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}"

class UserList(db.Model):
    """A user's List."""

    __tablename__ = "userLists"

    userlist_id = db.Column(db.Integer,
                            autoincrement=True,
                            primary_key=True)
    name = db.Column(db.String)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"))
    
    formMaps = db.relationship("FormMap", back_populates="userlist")
    user = db.relationship("User", back_populates="userlists")
    
    def __repr__(self):
        return f"<UserList userlist_id={self.userlist_id} name={self.name}"



class FormMap(db.Model):
    """Media that makes up a User's list."""

    __tablename__ = "formMaps"

    formMap_id = db.Column(db.Integer,
                            autoincrement=True,
                            primary_key=True)
    userlist_id = db.Column(db.Integer,
                            db.ForeignKey("userLists.userlist_id"))
    form_id = db.Column(db.Integer,
                        db.ForeignKey("forms.form_id"))
    
    userlist = db.relationship("UserList", back_populates="formMaps")
    form = db.relationship("Form", back_populates="formMap")
    
    def __repr__(self):
        return f"<FormMap formMap_id_id={self.formMap_id} form_id={self.form_id}"


class Form(db.Model):
    """A form."""

    __tablename__ = "forms"

    form_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    media_id = db.Column(db.Integer,
                        db.ForeignKey("medias.media_id"))
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"))
    rating = db.Column(db.Integer)
    thoughts = db.Column(db.Text)
    recommend_or_not = db.Column(db.String)
    created_at = db.Column(db.DateTime)

    media = db.relationship("Media", back_populates="forms")
    user = db.relationship("User", back_populates="forms")
    formMap = db.relationship("FormMap", back_populates="form")

    def __repr__(self):
        return f"<Form form_id={self.form_id} created_at={self.created_at}>"


class Media(db.Model):
    """A specific media."""

    __tablename__ = "medias"

    media_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    # mediatype_id = db.Column(db.Integer,
    #                         db.ForeignKey("mediaTypes.mediatype_id"))
    type = db.Column(db.String)
    name = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.Text)

    # mediatype = db.relationship("MediaType", back_populates="media")
    forms = db.relationship("Form", back_populates="media")

    def __repr__(self):
        return f"<Media media_id={self.media_id} name ={self.name}>"


# class MyEnum(enum.Enum):
#     webcomic = 1
#     book = 2
#     tv = 3
#     movie = 4


# class MediaType(db.Model):
#     print('MEDIA TYPE')
#     """A media type."""

#     __tablename__ = "mediaTypes"

#     mediatype_id = db.Column(db.Integer,
#                             autoincrement=True,
#                             primary_key=True)
#     type = db.Column(db.Enum(MyEnum))

#     media = db.relationship("Media", back_populates="mediatype")

#     def __repr__(self):
#         return f"<MediaType mediatype_id={self.mediatype_id} type={self.type}>"







def connect_to_db(flask_app, db_uri="postgresql:///consumedmedia", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)






