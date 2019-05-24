from models.user import UserModel



def authenticate(username,password):
    #.get is another way of accessing a python dictionary. if there is not such username, user will be returned as None

    user = UserModel.find_by_username(username)
    if user and user.password == password:
        return user

#payload is the content of the JWT token

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
