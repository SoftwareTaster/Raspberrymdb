#!/usr/bin/env python
# encoding: utf-8

from flask import Flask, request, render_template
from flask.ext.restful import Resource, Api

app = Flask(__name__)
api = Api(app)

todos = {}

class TodoSimple(Resource):
    def get(self, todo_id):
        return {'hello': 'the world'}

    def post(self, todo_id):
        todos[todo_id] = request.form['lastname']
        return todos[todo_id]

api.add_resource(TodoSimple, '/<string:todo_id>')

@app.route('/')
def hello_world():
    return render_template('a.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')