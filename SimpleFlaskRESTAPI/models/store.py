from db import db

class StoreModel(db.Model):

    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    # so that each time a store is created, the relationship does not need to be created, so until items is used somewhere
    # (i.e. the json method below). items are not stored in the store table
    # many items is linked to one store
    items = db.relationship("ItemModel", lazy='dynamic')


    def __init__(self, name):
        self.name = name

    #using self.items.all will force the function to look into the db everytime .json is called. so it costs time.
    # so there's a tradeoff between speed of calling the json method and speed of creating store object
    def json(self):
        # self.item here is a query builder that has the ability to look into the table,
        # it does not return the items object, so we use .all to retrive the items in the table
        return {'name': self.name, 'items': list(map(lambda x: x.json(), self.items.all()))}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):

        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):

        db.session.delete(self)
        db.session.commit()