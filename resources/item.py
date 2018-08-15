from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='Price cannot be empty')
    parser.add_argument('store_id', type=int, required=True, help='Store id cannot be empty')

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name, store_id)
        return item.json() if item else {'message': 'Item not found'}, 404
    
        
    
    def post(self, name):
        data = Item.parser.parse_args()
        if ItemModel.find_by_name(name):
            return {'message': 'Item with name {} already exists.'.format(name)}, 400       
        
        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {'message': 'Internal server error creating item'}, 500

        return item.json(), 201 
    
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()     
            
        return {'message': 'Item deleted'}, 200
    
    def put(self, name):
        
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if not item:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.store_id = data['store_id']
        
        item.save_to_db()
            
        return item.json(), 200           


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}