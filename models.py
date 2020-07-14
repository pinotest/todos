import json


class Todos:
    def __init__(self):
        try:
            with open("todos.json", "r") as f:
                self.todos = json.load(f)
        except FileNotFoundError:
            self.todos = [
                {
                    'title': 'Zakupy',
                    'description': 'Mleko, jajka, mąka, olej, papier toaletowy (jak będzie)',
                    'done': False
                },
                {
                    'title': 'Zrobić zadania z Pythona',
                    'description': 'Przygotować projekt z modułu i wysłać Mentorowi',
                    'done': False
                }
            ]

    def all(self):
        return self.todos

    def get(self, id):
        return self.todos[id]

    def create(self, data):
        data.pop('csrf_token')
        self.todos.append(data)

    def save_all(self):
        with open("todos.json", "w") as f:
            json.dump(self.todos, f)

    def update(self, id, data):
        data.pop('csrf_token')
        self.todos[id] = data
        self.save_all()


todos = Todos()
