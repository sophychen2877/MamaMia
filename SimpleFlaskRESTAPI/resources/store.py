from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.store import StoreModel

class Store(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help='Store name cannot be left blank')

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'store not found'}, 404

    def post(self, name):

        result = StoreModel.find_by_name(name)

        if result:
            return {'message': f'store with name {name} already exists '}, 400

        data = Store.parser.parse_args()
        store = StoreModel(data['name'])

        try:
            store.save_to_db()
        except:
            return {'message': 'an error occurs when trying to save the item to database'}, 500

        return store.json(), 201


    def delete(self, name):
        store = StoreModel.find_by_name(name)

        if store is None:
            return {'message': f'store with name {name} does not exist'}, 404

        try:
            store.delete_from_db()
        except:
            return {'message': 'an error occured when trying to delete the item from database'}, 500

        return {'message': 'Store Deleted'}



class StoreList(Resource):

    def get(self):

        return {'stores': list(map(lambda x: x.json(), StoreModel.query.all()))}



