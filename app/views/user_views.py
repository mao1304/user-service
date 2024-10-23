from flask_restx import Resource, Namespace

user_routes = Namespace('user_routes', description='routes for users')

@user_routes.route('/test')
class test(Resource):
    def get(self):
        return {'message': 'This is a test'}
    # def post(self):
    