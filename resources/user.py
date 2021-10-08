import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel
from db import db


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='This field cannot be left blank'
                        )

    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='This field cannot be left blank')

    def post(self):
        # data = request.get_json()
        data = UserRegister.parser.parse_args()
        username = data['username']
        password = data['password']
        # Check if the user already exists
        user = UserModel.find_by_username(username)

        if user:  # If the user already exists
            return {"message": "User already exists"}

        user = UserModel(username, password)
        user.save_to_db()

        return {"message": "The user created successfully"}
