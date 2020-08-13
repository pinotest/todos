from flask import Flask, jsonify, abort, make_response, request, redirect, render_template, url_for
from forms import TodoForm
from TodosSQLite import todos
import logging

import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

app = Flask(__name__)
app.config["SECRET_KEY"] = "nietaknietaknietak"


@app.route("/api/v1/todos/", methods=["GET"])
def todos_list_api_v1():
    # issue zwraca jedynie zawartość tabeli - nie ma klucza w json
    return jsonify(todos.select_all())


@app.route("/api/v1/todos/<int:todo_id>", methods=["GET"])
def get_todo(todo_id):
    todo = todos.get(todo_id)
    if not todo:
        abort(404)
    return jsonify({"todo": todo})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)


@app.route("/api/v1/todos/", methods=["POST"])
def create_todo():
    if not request.json or not 'title' in request.json:
        abort(400)
    todo = {
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    todos.create(todo)
    return jsonify({'todo': todo}), 201


@app.route("/api/v1/todos/<int:todo_id>", methods=['DELETE'])
def delete_todo(todo_id):
    result = todos.delete(todo_id)
    if not result:
        abort(404)
    return jsonify({'result': result})


@app.route("/api/v1/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    todo = todos.get(todo_id)
    if not todo:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'title' in data and not isinstance(data.get('title'), str),
        'description' in data and not isinstance(data.get('description'), str),
        'done' in data and not isinstance(data.get('done'), bool)
    ]):
        abort(400)
    todo = {
        'title': data.get('title', todo['title']),
        'description': data.get('description', todo['description']),
        'done': data.get('done', todo['done'])
    }
    todos.update(todo_id, todo)
    return jsonify({'todo': todo})

# web version


@app.route("/todos/", methods=["GET", "POST"])
def todos_list():
    form = TodoForm()
    error = ""
    if request.method == "POST":
        if form.validate_on_submit():
            response = requests.post(str(request.url_root) + url_for("create_todo"),
                                     json=form.data, headers={'Content-type': 'application/json',
                                                              'Accept': 'text/plain'})
            logging.info("response %s" % response.status_code)
            if response.status_code != 201:
                logging.error("Technical problem with API funcion")
    return render_template("todos.html", form=form, todos=todos.select_all(), error=error)


@ app.route("/todos/<int:todo_id>/", methods=["GET", "POST"])
def todo_details(todo_id):
    todo = todos.get(todo_id)
    form = TodoForm(data=todo)
    if request.method == "POST":
        todos.update(todo_id, form.data)
        return redirect(url_for("todos_list"))
    return render_template("todo.html", form=form, todo_id=todo_id)


if __name__ == "__main__":
    app.run(debug=True)
