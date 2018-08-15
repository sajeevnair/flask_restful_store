from models import UserModel
from flask_restful import Resource, reqparse

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="Username cannot be empty" )
    parser.add_argument('password', type=str, required=True, help="Password cannot be empty" )
    
    def post(self):
        data = UserRegister.parser.parse_args()
     
        if UserModel.find_by_username(data['username']): 
            return {"message": "user already exists."}

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully"}, 201