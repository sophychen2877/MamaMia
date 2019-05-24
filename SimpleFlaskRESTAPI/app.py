from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList


##sensitive information masked for security reasons
DB_TYPE = 'mysql'
DB_DRIVER = 'pymysql'
DB_USER = '#######'
DB_PASS = '########'
DB_HOST = '######'
DB_PORT = '3306'
DB_NAME = '#####'
POOL_SIZE = 50
SQLALCHEMY_DATABASE_URI = f'{DB_TYPE}+{DB_DRIVER}://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

#create app
app = Flask(__name__)
#noted this URI can be changed
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #turn the flask modification setting off to save some computing resouces (sqlalchemy has its own modification tracker)
app.secret_key = 'secrets_keys'


#sqlalchemy to create tables. this relies on the imported modules (Store/StoreList resource, and in which imports the Store/StoreList Models) Store/StoreList models
# will create tables





#authentication -  JWT object creates a new endpoint /auth
jwt = JWT(app, authenticate, identity)


api = Api(app)
api.add_resource(Item,'/item/<string:name>') # http://127.0.0.1:5000/item/<string:name>
api.add_resource(ItemList, '/items') # http://127.0.0.1:5000/items
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    with app.test_request_context():
        db.create_all()
    app.run(port=5000, debug=True)
