#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource

from config import app, db, api
from models import User

class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204

class Signup(Resource):
    def post(self):
        data = request.get_json()
        username= data['username']
        password = data['password']

        if username and password:
            user = User(username=username)
            user.password_hash = password

            db.session.add(user)
            db.session.commit()

            session['user_id'] = user.id

            return user.to_dict(), 201
    
api.add_resource(Signup, '/signup')

class CheckSession(Resource):
    def get(self):

        if session.get('user_id'):
            user = User.query.filter(User.id == session['user_id']).first()
            return user.to_dict(), 200
        
        return {}, 204
        
api.add_resource(CheckSession, '/check_session')

class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']

        user = User.query.filter(User.username == username).first()

        if user.authenticate(password):
            session['user_id'] = user.id

            return user.to_dict(), 200

api.add_resource(Login, '/login')

class Logout(Resource):
    def delete(self):
        session['user_id'] = None
        return {}, 204

api.add_resource(Logout, '/logout')
api.add_resource(ClearSession, '/clear', endpoint='clear')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
