from flask_restful import Resource

from section4.code.models.store_model import StoreModel


class Store(Resource):
    def get(self, name):
        try:
            store = StoreModel.find_by_name(name)
        except:
            return {'message': 'An error occurred finding the store.'}, 500

        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "An store with '{}' already exists.".format(name)}, 400  # bad request
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': 'An error occurred while creating the store.'}, 500  # Internal server error

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {'message': 'Store deleted'}


class StoreList(Resource):
    def get(self):
        return {'stores': list(map(lambda store: store.json(), StoreModel.query.all()))}
