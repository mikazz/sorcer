from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class App(Resource):
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}


api.add_resource(App, '/')

if __name__ == '__main__':
    app.run(debug=True)
