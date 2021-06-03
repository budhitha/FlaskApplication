from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from flask_restful import Resource, reqparse

from models.item_model import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='This field cannot be left blank!')
    parser.add_argument('store_id', type=int, required=True, help='Every item needs a store id.')

    @jwt_required()
    def get(self, name):
        try:
            item = ItemModel.find_by_name(name)
        except:
            return {'message': 'An error occurred finding the item.'}, 500
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    @jwt_required(refresh=True)
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with '{}' already exists.".format(name)}, 400  # bad request

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {'message': 'An error occurred inserting the item.'}, 500  # Internal server error

        return item.json(), 201  # 201 - Created | 202 - Accepted (when creation delay)

    @jwt_required()
    def delete(self, name):
        claims = get_jwt()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required!'}, 401
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
            item.save_to_db()
        else:
            item.price = data['price']
            item.store_id = data['store_id']
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    @jwt_required(optional=True)
    def get(self):
        user_id = get_jwt_identity()
        items = list(map(lambda item: item.json(), ItemModel.find_all()))
        if user_id:
            return {'items': items}
        return {'items': [item['name'] for item in items],
                'message': 'More data available if you log in.'}
