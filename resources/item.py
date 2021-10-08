import pyodbc
from flask_restful import Resource, reqparse
import sqlite3
from flask_jwt import JWT, jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('color', type=str, required=False, help="Color is optional")

    parser.add_argument('store_id', type=int, required=True, help="Store ID of store where this item resides cannot "
                                                                  "be blank")

    @jwt_required()  # this means we must authenticate before calling get method
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200 if item else 404  # this is to ensure that the output is a valid json

        return {"message": "Item not found"}

    def post(self, name):

        item = ItemModel.find_by_name(name)

        if item is not None:
            return {"message": "Item with the same name already exists"}, 400  # 400 is a bad request

        # data = request.get_json(force=True)
        # force=True means that the Content-Type header is not needed.
        # API will fetch contents from body irrespective of the content type set.
        # data = request.get_json()
        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'], data['store_id'])
        try:
            item.save_to_db()
        except Exception:
            return {"Message": "An error occurred while inserting item."}, 500
        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {"Message": "Item has been deleted"}

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:  # No item exists with this name
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']

        item.save_to_db()
        return item.json(), 200


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
