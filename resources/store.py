from flask_restful import Resource
from models.store import StoreModel


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200

        return {'message':'No such store found'}, 404
        pass

    def post(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return {'message':'A store with the same name already exists'}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except Exception:
            return {'message':'An internal error has occurred while saving the store in database'}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {'message':'The store has been deleted'}

        return {'message':'The store does not exists'}, 400


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
