from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
    type = float,
    required = True,
    help = "This field is mandatory" )

    #@jwt_required()
    def get(self, name):
        item  = ItemModel.find_by_name(name)

        if item:
            return item.json(), 200
        else:
            return {'message': 'Item not found'}, 404


    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists".format(name)}, 400

        request_data = Item.parser.parse_args()

        item = ItemModel(name, request_data['price'])

        try:
            item.insert()
        except:
            return {"message": "An error occurred while inserting item"}, 500

        return item.json(), 201


    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE name=?"

        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return{'message': 'item deleted'}, 204



    def put(self, name):
        request_data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, request_data['price'])

        if item:
            try:
                updated_item.update()
            except:
                return {"message": "An error occurred while updating item"}, 500
        else:
            try:
                updated_item.insert()
            except:
                return {"message": "An error occurred while inserting item"}, 500

        return updated_item.json()


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"

        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        connection.close()
        return {"items": items}