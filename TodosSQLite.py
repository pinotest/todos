import sqlite3
import logging
from sqlite3 import Error
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')


class TodosSQLite:
    def __init__(self, db_file="todos.db"):
        self.db_file = db_file

    def cursor(self):
        self.conn = self.create_connection()
        return self.conn.cursor()

    def create_connection(self):
        """ create a database connection to the SQLite database
            specified by db_file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_file)
            logging.info("Successfully Connected to SQLite")
            return conn
        except Error as e:
            logging.error("Technical problem: %s" % e)
        return conn

    def count_all(self):
        cur = self.cursor().execute(f"SELECT max(id) FROM todos;")
        todos_list = cur.fetchall()
        cur.close()  # dodać zamkniecie połączenie z baza za każdym razem?
        return todos_list

    def select_all(self):
        """
        Query all rows in the table
        return:
        """
        cur = self.cursor()
        cur.execute("SELECT * FROM todos")
        rows = cur.fetchall()
        cur.close()
        return rows

    def get(self, id):
        cur = self.cursor()
        cur.execute("SELECT * FROM todos WHERE id==?", (id,))
        todo = cur.fetchall()
        convert_todo = {'id': todo[0][0], 'title': todo[0][1],
                        'description': todo[0][2], 'done': todo[0][3]}
        if todo:
            return convert_todo
        cur.close()
        return {}

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
        cur.close()
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
            cur.close()
            logging.info("Update done succesfully")
        except sqlite3.OperationalError as e:
            logging.error("Technical problem: %s" % e)

    def delete(self, id):
        #     """
        #     Delete existing todo in the todos table
        #     :param todo id: id
        #     :return: True
        #     """
        todo = self.get(id)
        if todo:
            sql = f'''DELETE from todos
                    WHERE id = ?'''
            try:
                cur = self.cursor()
                cur.execute(sql, (id, ))
                self.conn.commit()
                cur.close()
                logging.info("Delete done")
            except sqlite3.OperationalError as e:
                logging.error("Technical problem: %s" % e)
            return True
        return False


todos = TodosSQLite()
