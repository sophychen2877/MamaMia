from db import db


class UserModel(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):

        self.username = username
        self.password = password

    #find the username within the users db
    @classmethod
    def find_by_username(cls, username):

        #use sqlite
        '''
        connection = sqlite3.connect('./data.db')
        cursor = connection.cursor()

        select_query = 'SELECT * FROM users WHERE username=?'
        result = cursor.execute(select_query, (username,))
        row = result.fetchone()
        if row:
            #since we're creating an instance of the User class, can just pass in the
            #sets of args as positional arguments as in user init method
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user
        '''

        #use sqlalchemy
        return cls.query.filter_by(username=username).first()


    # find the userid within the users db
    @classmethod
    def find_by_id(cls, _id):

        #use sqlite
        '''
        connection = sqlite3.connect('./data.db')
        cursor = connection.cursor()

        select_query = 'SELECT * FROM users WHERE id=?'
        result = cursor.execute(select_query, (_id,))
        row = result.fetchone()
        if row:
            # since we're creating an instance of the User class, can just pass in the
            # sets of args as positional arguments as in user init method
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user
        '''

        # use sqlalchemy
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

