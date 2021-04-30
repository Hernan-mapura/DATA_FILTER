from flask.views import MethodView
from flask import jsonify, request
from bot.send import SendMailToCollaborators
from models.environment import Environment
import bcrypt
import jwt
from config import KEY_TOKEN_AUTH
import datetime


class CreateEnvironment(MethodView):
    def post(self):
        environ = Environment() 
        content = request.get_json()
        print(content)
        environ.name = content.get('name')
        environ.img = content.get('img')
        environ.key_code = content.get('key_code')
        environ.created_by = content.get('created_by')
        answer = environ.create()
        return jsonify(), 200

class ShowEnvironment(MethodView):
    def post(self):
        environ = Environment()
        content = request.get_json()
        environ.id = content.get('id')
        answer = environ.show()
        if(answer):
            return jsonify(answer), 200
        else:
            return jsonify(), 400

class RemoveEnvironment(MethodView):
    def post(self):
        environ = Environment()
        content = request.get_json()
        environ.id = int(content)
        answer = environ.remove()
        return jsonify(), 200

class SearchEnvironment(MethodView):
    def post(self):
        environ = Environment()
        content = request.get_json()
        environ.id = content.get('id')
        environ.name = "%" + content.get('search') + "%"
        answer = environ.search_environment()
        if(answer):
            return jsonify(answer),200
        else:
            return jsonify(),400


class ManageUsers(MethodView):
    def get(self,id):
        environ = Environment()
        environ.id = int(id)
        answer = environ.manega_users_show()
        return jsonify(answer), 200

class ManageUsersRemove(MethodView):
    def post(self):
        environ = Environment()
        content = request.get_json()
        environ.id = content.get('id')
        answer = environ.manega_users_remove()
        print(answer)
        return jsonify(), 200

class JoinByCode(MethodView):
    def post(self):
        environ = Environment()
        content = request.get_json()
        environ.key_code = content.get('key_code')
        environ.id = content.get('id_user')
        answer = environ.manage_user_join_by_Code()
        if(answer == "stError"):
            return jsonify({'status':'stError'}), 200
        else:
            if(answer == "stError101"):
                return jsonify({'status':'stError101'}), 200
            else:
                return jsonify({'status':'good'}),200

class SearchManage(MethodView):
    def post(self):
        environ = Environment()
        content = request.get_json()
        environ.name = '%' + content.get('search') + '%'
        environ.id = content.get('id_environment')
        answer = environ.manage_search()
        if(answer):
            return jsonify(answer), 200
        else:
            return jsonify(), 500

class SendMailCollaborators(MethodView):
    def post(self):
        environ = Environment()
        content = request.get_json()
        users = content.get('users')
        environment = content.get('environment')
        if(users != ['','','']):
            answer = environ.manage_search_email(users)
            if(answer):
                for i in answer:
                    SendMailToCollaborators(i)
                return jsonify(answer), 200
            else:
                return jsonify({"status":100}), 200
        else:
            return jsonify(), 400