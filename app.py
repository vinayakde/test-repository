from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList


print("Imported Item, ItemList")
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'jose'

api = Api(app)
jwt = JWT(app, authenticate, identity)


"""
jwt creates a new endpoint /auth to which we send user id and password
jwt invokes authenticate function on the user id and password to ger user object.
On successful retrieval of user object, jwt returns a jwt token. 
This token could be sent along with subsequent requests. 
JWT calls identity function with this token to get correct user id and user object.
"""
items = []

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__':
    # print("Importing db")
    from db import db

    db.init_app(app)
    app.run(port=5000, debug=True)
