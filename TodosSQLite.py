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
        todos_list = cur.fetchall()
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
        cur = self.cursor()
        cur.execute("select * from todos where id==?", (id,))
        todo = cur.fetchall()

        convert_todo = {'id': todo[0][0], 'title': todo[0][1],
                        'description': todo[0][2], 'done': todo[0][3]}
        if todo:
            return convert_todo
        return []

    def create(self, data):
        #     """
        #     Add a new todo into the todos table
        #     :param new todo: data
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
        #     """
        #     Update existing todo in the todos table
        #     :param todo id: id
        #     :param new data for todo: data
        #     """
        if data['done'] == False:
            data['done'] = 0
        else:
            data['done'] = 1
        sql = f'''UPDATE todos
                    SET title='{data['title']}', description='{data['description']}', done={data['done']}
                    WHERE id = ?'''
        try:
            cur = self.cursor()
            cur.execute(sql, (id, ))
            self.conn.commit()
            print("Update wykonany")
        except sqlite3.OperationalError as e:
            print("Problem techniczny: ", e)

    def delete(self, id):
        #     """
        #     Delete existing todo in the todos table
        #     :param todo id: id
        #     :param new data for todo: data
        #     """
        todo = self.get(id)
        if todo:
            sql = f'''DELETE from todos
                    WHERE id = ?'''
            try:
                cur = self.cursor()
                cur.execute(sql, (id, ))
                self.conn.commit()
                print("Delete wykonany")
            except sqlite3.OperationalError as e:
                print("Problem techniczny: ", e)
            return True
        return False


todos = TodosSQLite()
