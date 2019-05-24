from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


#in restful, when returnina dictionary like json, just return the dictionary and no need to jsonify it anymore, as restful will do it for you
class Item(Resource):

    # parser can parse the payload information, so only the desired data be retrieved as data and then updated
    # parser looks at json payload, but also the form payload
    # required=True garentees no request comes through if there's no price in the payload
    # so if you have a parser, you do not need get_json() to get the payload
    # data = request.get_json()
    # parser can belong to a class so there's no need to update the codes in each methods if needed
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='This field cannot be left blank')
    parser.add_argument('store_id', type=int, required=True, help='Every item needs a store id')

    #@jwt_required
    def get(self, name):
        #if i'm calling a classmethod
        result = ItemModel.find_by_name(name)
        if result:
            # since we're creating an instance of the User class, can just pass in the
            # sets of args as positional arguments as in user init method
            return result.json()

        return {'message': 'item not found'}, 404



        #here to use filter when we dont have a database setup yet for the itmes but to use a global variable items as a list to store all items
        #hence using filter on lambda function to find the item
        
        #use next with filter (because there's only going to be one item, otherwise usually can wrap a list around filter,
        # so python doesn't return a filter object
        # include None in the next function so when there is no object to return, it does not break the program but only to return None

        #item = next(filter(lambda x: x['name'] == name, items), None)

        # return 404 status code if the item is not found
        #return {'item': item}, 200 if item else 404




#noted that restful only recognize default function name such as post, get, delete, put etc, so if you update the function name to post_item, restful will thrw
# out error message
    #@jwt_required()
    def post(self, name):

        result = ItemModel.find_by_name(name)

        if result:
            return {'message': f'item with name {name} already exists '}, 400

        data = Item.parser.parse_args()  # data here is a json object with only 'price' element
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            #http code 500 - internal server error
            return {'message': 'an error occurs when trying to insert the item'}, 500

        return item.json(), 201


        # force=True means you do not need the content_type header (which is set to application/json in postman)
        # this is dangerous because once you force the content_type header to True then it only looks at the body, if the format is not
        # correct then you do nothing so do not use force=True

        #another parameter to deal with error is silence = True, this makes sure that the error will not be displayed but returns null
        #so do not use it either
        #global items
        #error first apprach -> deal with error first, then do the rest when there's no error
        #if next(filter(lambda x: x['name'] == name, items), None):
        #   return {'message': f'item with name {name} already exists '}, 400

        #data = Item.parser.parse_args()  # data here is a json object with only 'price' element
        #item = {'name': name, 'price': data['price']}
        #items.append(item)
        #when create a new item, set the http status code to 201
        # can also set status code to 202 accepted, when it takes certain amount of time for server to accept the new item
        #return item, 201

    def delete(self, name):
        result = ItemModel.find_by_name(name)

        if result is None:
            return {'message': f'item with name {name} does not exist'}, 404

        try:
            result.delete_from_db()
        except:
            return {'message': 'an error occured when trying to delete the item'}, 500

        return {'message': 'item has been deleted'}

    def put(self, name):

        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        # if the item does not exist, insert the item to db
        if item:
            item.price = data['price']
            item.store_id = data['store_id']

        try:
            item = ItemModel(name, **data)
        except:
            return {'message': 'an error occurs when trying to insert the item'}, 500

        item.save_to_db()

        return item.json()


class ItemList(Resource):

    #@jwt_required()
    def get(self):

        #user sqlite
        '''
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        select_query = 'SELECT * FROM items'
        result = cursor.execute(select_query)
        items = []

        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        connection.close()

        if len(items) > 0:
            return {'items': items}
        return {'items': None}, 404
        '''

        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}



