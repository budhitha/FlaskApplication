import sqlite3

from flask_jwt import jwt_required
from flask_restful import Resource, reqparse


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='This field cannot be left blank!')

    @jwt_required()
    def get(self, name):
        try:
            item = self.find_by_name(name)
        except:
            return {'message': 'An error occurred finding the item.'}, 500
        if item:
            return item
        return {'message': 'Item not found'}, 404

        # item = next(filter(lambda element: element['name'] == name, items), None)  # first item filter by this function
        # return {'item': item}, 200 if item is not None else 404
        # # for item in items:
        # #     if item['name'] == name:
        # #         return item
        # # return {'item': None}, 404  # 404 - Not found

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('storeData.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM items WHERE name  = ?'
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}

    def post(self, name):
        if self.find_by_name(name):
            return {'message': "An item with '{}' already exists.".format(name)}, 400  # bad request

        data = Item.parser.parse_args()

        item = {'name': name, 'price': data['price']}

        try:
            self.insert(item)
        except:
            return {'message': 'An error occurred inserting the item.'}, 500  # Internal server error

        return item, 201  # 201 - Created | 202 - Accepted (when creation delay)

        # if next(filter(lambda element: element['name'] == name, items), None):
        #     return {'message': "An item with '{}' already exists.".format(name)}, 400  # bad request
        #
        # # data = request.get_json()
        # data = Item.parser.parse_args()
        #
        # item = {'name': name, 'price': data['price']}
        # items.append(item)
        # return item, 201  # 201 - Created | 202 - Accepted (when creation delay)

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('storeData.db')
        cursor = connection.cursor()

        query = 'INSERT INTO items VALUES (?,?)'
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    def delete(self, name):
        connection = sqlite3.connect('storeData.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE `name` = ?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()
        # global items
        # items = list(filter(lambda item: item['name'] != name, items))

        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        # data = request.get_json()

        item = self.find_by_name(name)
        # item = next(filter(lambda x: x['name'] == name, items), None)

        updated_item = {'name': name, 'price': data['price']}

        if item is None:
            try:
                self.insert(updated_item)
                # items.append(item)
            except:
                return {'message': 'An error occurred inserting the item'}, 500
        else:
            try:
                self.update(updated_item)
                # item.update(data)
            except:
                return {'message': 'An error occurred updating the item'}, 500
        return updated_item

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('storeData.db')
        cursor = connection.cursor()

        query = 'UPDATE items SET price=? where `name`=?'
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('storeData.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM items'
        result = cursor.execute(query)

        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        connection.close()

        return {'items': items}
