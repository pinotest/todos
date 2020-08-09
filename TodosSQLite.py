import sqlite3
from sqlite3 import Error


class TodosSQLite:
    def __init__(self, db_file="todos.db"):
        self.db_file = db_file

    def cursor(self):
        self.conn = self.create_connection(self.db_file)
        return self.conn.cursor()

    def create_connection(self, db_file):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            print("Successfully Connected to SQLite")
            return conn
        except Error as e:
            print(e)
        return conn

    def count_all(self):
        cur = self.cursor().execute(f"SELECT max(id) FROM todos;")
        print("cur", cur)
        todos_list = cur.fetchall()
        print("cur.fetchall()", cur.fetchall())
        print("cur.execute", cur.execute("select id from todos;"))
        print("cur.fetchall()", cur.fetchall())
        cur.close()
        return todos_list

    def select_all(self):
        """
        Query all rows in the table
        return:
        """
        cur = self.cursor()
        cur.execute("SELECT * FROM todos")
        rows = cur.fetchall()
        return rows

    def get(self, id):
        # todo = [todo for todo in self.select_all() if todo['id'] == id]
        todo = self.select_all()
        print(todo)
        if todo:
            return todo[0]
        return []

    def create(self, data):
        #     """
        #     Add a new todo into the todos table
        #     :param todo:
        #     :return: todo id
        #     """
        sql = '''INSERT INTO todos(title, description, done)
                VALUES(?,?,?)'''
        cur = self.cursor()
        data = (data['title'], data['description'], data['done'])
        cur.execute(sql, data)
        self.conn.commit()
        return cur.lastrowid

    def update(self, id, data):
        todo = self.get(id)
        if todo:
            index = self.todos.index(todo)
            self.todos[index] = data
            return True
        return False

    # def delete(self, id):
    #     todo = self.get(id)
    #     if todo:
    #         self.todos.remove(todo)
    #         self.save_all()
    #         return True
    #     return False


todos = TodosSQLite()
# todos.create_connection("database.db")
