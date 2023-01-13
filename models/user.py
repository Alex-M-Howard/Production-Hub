from db import db

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()


class User(db.Model):
    """ 
            USER MODEL
    ID           : Primary Key
    First Name   : String
    Last Name    : String
    Email        : String
    Password     : String -> Bcrypt to hash
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String, nullable=False, unique=False)
    last_name = db.Column(db.String, nullable=False, unique=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    isadmin = db.Column(db.Boolean, nullable=False, default=False)
    role = db.Column(db.String, nullable=False, default='user')

    def __repr__(
        self): return f"<User #{self.id}: {self.first_name} {self.last_name}, {self.email}>"

    def name(self):
        return f"{self.first_name} {self.last_name}"

    @classmethod
    def signup(cls, first_name, last_name, email, password):
        """
          Hash password using Bcrypt
          Create New User
          Add to DB
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_pwd
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, email, password):
        """
        Find user with provided email and password

        If found -> return user
        Else     -> return False
        """

        user = cls.query.filter_by(email=email).first()

        if user:
            is_authorized = bcrypt.check_password_hash(user.password, password)
            if is_authorized:
                return user

        return False

    @classmethod
    def new_password(cls, email, password):
        """
        Hash password using Bcrypt
        Update password
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = cls.query.filter_by(email=email).one()
        user.password = hashed_pwd

        db.session.add(user)
        db.session.commit()

        return user
