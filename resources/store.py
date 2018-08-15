from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models import StoreModel

class Store(Resource):
    
    def get(self, name):
        store = StoreModel.find_by_name(name)
        return store.json() if store else {'message': 'Store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': 'The store with name {} already exists'.format(name)}, 400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': 'Internal server error creating store'}, 500

        return store.json(), 200

    def delete(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            store.delete_from_db()
        
        return {'message': 'store deleted'}


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}