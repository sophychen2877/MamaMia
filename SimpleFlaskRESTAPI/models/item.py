from db import db

class ItemModel(db.Model):

    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    # one item can only be sold in one store
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    #hence one single store
    store = db.relationship("StoreModel")


    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price, 'store_id': self.store_id}

    @classmethod
    def find_by_name(cls, name):

        #use sqlite
        '''
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        select_query = 'SELECT * FROM items WHERE name=?'
        result = cursor.execute(select_query, (name,))
        row = result.fetchone()
        connection.close()
        if row:
            # since we're creating an instance of the User class, can just pass in the
            # sets of args as positional arguments as in user init method
            return cls(*row)

        return None
        '''
        #use sqlalchemy
        return cls.query.filter_by(name=name).first()


    #under sqlite this method was a insert function
    def save_to_db(self):

        #use sqlite
        '''
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        insert_query = 'INSERT INTO items VALUES (?,?)'
        cursor.execute(insert_query, (self.name, self.price))
        connection.commit()
        connection.close()
        '''

        #use sqlalchemy
        #this does to both insert and update new items as now the primary key has changed to id
        db.session.add(self)
        db.session.commit()


    #use sqlite. this method is combined to save_to_db (previously insert)
    '''
    def update(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        update_query = 'UPDATE items SET price=? WHERE name=?'
        cursor.execute(update_query, (self.price, self.name))
        connection.commit()
        connection.close()
    '''

    #previously delete method
    def delete_from_db(self):

        #use sqlite
        '''
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        delete_query = 'DELETE FROM items WHERE name=?'
        cursor.execute(delete_query, (name,))
        connection.commit()
        connection.close()
        '''

        #use sqlalchemy
        db.session.delete(self)
        db.session.commit()



