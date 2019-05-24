import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel



class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='username cannot be left blank')
    parser.add_argument('password', type=str, required=True, help='password cannot be left blank')

    def post(self):

        data = UserRegister.parser.parse_args()
        # before new user information logged into the database, check if it's duplicate
        if UserModel.find_by_username(data['username']):
            return {'message': 'this username has already been registered, use a different username'}, 400

        new_user = UserModel(**data)


        #use sqlite
        '''
        connection = sqlite3.connect('./data.db')
        cursor = connection.cursor()
        #id is self-incrementing, therefore setting it to null
        insert_query = 'INSERT INTO users VALUES (NULL,?,?)'
        cursor.execute(insert_query, (data['username'], data['password']))

        connection.commit()
        connection.close()
        '''
        try:
            new_user.save_to_db()
        except:
            return {'message': 'an error occur when trying to save new user to the database '}

        return {'message': 'user created successfully'}, 201






