import sqlite3

from flask import g


class FlaskDb:
    def __init__(self, db_file_name: str) -> None:
        self.db_file_name = db_file_name

    def open(self):
        self.conn = sqlite3.connect(self.db_file_name)
        self.cursor = self.conn.cursor()

    def close(self):
        if hasattr(self, 'conn'):
            self.conn.close


class DefaultInterface:
    def get_write_data(self, **kwargs):
        columns = []
        values = []
        for key, value in kwargs.items():
            if value is not None:
                columns.append(key)
                values.append(value)
        if columns:
            name_of_columns = ', '.join(columns)
            insert_times = ''
            for _ in values:
                insert_times += '?,'
            insert_times = insert_times[:len(insert_times)-1]
            return name_of_columns, insert_times, columns, values
        return None, None, None, None

    def connect(self, db_base: FlaskDb):
        self.conn = db_base.conn
        self.cursor = db_base.cursor


class CategoryDb(DefaultInterface):
    #**Категорія**
    # 1. Назва - Текст/варчар **req**
    # 2. Детальний опис категорії - текст **not req**
    # 3. Колір - варчар (default - some color)
    def create_default_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS category (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(64) NOT NULL,
                description TEXT,
                color VARCHAR(32)
            )
        """)
        self.conn.commit()

    def get_categories(self):
        self.cursor.execute("""
            SELECT id, name, description, color FROM category
        """)
        return self.cursor.fetchall()

    def get_category(self, id):
        self.cursor.execute("""
            SELECT name, description, color FROM category WHERE id=?
        """, (id,))
        return self.cursor.fetchone()

    def create_category(self, **kwargs):
        name_of_columns, insert_times, columns, values = self.get_write_data(**kwargs)

        self.cursor.execute("""
            INSERT INTO category ({}) VALUES ({})
        """.format(name_of_columns, insert_times), values)

        self.conn.commit()

    def delete_category(self, id):
        self.cursor.execute("""
            DELETE FROM category WHERE id=?
        """, (id, ))

        self.conn.commit()

    def edit_category(self, id, **kwargs):
        name_of_columns, insert_times, columns, values = self.get_write_data(**kwargs)
        values.append(id)
        update_fields=''
        for name in columns:
            update_fields += f"{name}=?, "
        update_fields = update_fields[:len(update_fields)-2]


        self.cursor.execute("""
            UPDATE category 
            SET {} 
            WHERE id=?
        """.format(update_fields), values)

        self.conn.commit()


class SpendingsDb(DefaultInterface):
    def create_default_table(self):
        #1. Назва - Текст/варчар **req**
        # 2. Категорія -  Це окрема табличка (тут буде id) **not req**
        # 3. Дата - date **not req (default - today)**
        # 4. Сума витрат/зарплати - float **req**
        # 5. це Витрата/Зарплата - boolean (default - False)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS spending (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(64) NOT NULL,
                category_id INT,
                date DATE DEFAULT CURRENT_TIMESTAMP,
                spending TEXT,
                is_spending BOOLEAN,
                FOREIGN KEY(category_id) REFERENCES category(id)
            )
        """)
        self.conn.commit()

    def get_spendings(self):
        self.cursor.execute("""
            SELECT * FROM spending
        """)
        return self.cursor.fetchall()

    def get_spending(self, id):
        self.cursor.execute("""
            SELECT * FROM spending WHERE id=?
        """, (id,))
        return self.cursor.fetchone()

    def create_spending(self, **kwargs):
        name_of_columns, insert_times, columns, values = self.get_write_data(**kwargs)

        self.cursor.execute("""
            INSERT INTO spending ({}) VALUES ({})
        """.format(name_of_columns, insert_times), values)

        self.conn.commit()

    def delete_spending(self, id):
        self.cursor.execute("""
            DELETE FROM spending WHERE id=?
        """, (id, ))

        self.conn.commit()

    def edit_spending(self, id, **kwargs):
        name_of_columns, insert_times, columns, values = self.get_write_data(**kwargs)
        values.append(id)
        update_fields=''
        for name in columns:
            update_fields += f"{name}=?, "
        update_fields = update_fields[:len(update_fields)-2]


        self.cursor.execute("""
            UPDATE spending 
            SET {} 
            WHERE id=?
        """.format(update_fields), values)

        self.conn.commit()


def get_db(is_server_start=False):
    db = getattr(g, '_database', None)
    if db is None:
        flask_db = FlaskDb('test_db.db')
        flask_db.open()
        db = g._database = flask_db
        if is_server_start:
            g._category_db = CategoryDb()
            g._category_db.connect(flask_db)
            g._category_db.create_default_table()

            g._spendig_db = SpendingsDb()
            g._spendig_db.connect(flask_db)
            g._spendig_db.create_default_table()
    return db


def get_category_db():
    db = getattr(g, '_category_db', None)
    if db is None:
        flask_db = get_db()
        db = g._category_db = CategoryDb()
        g._category_db.connect(flask_db)
    return db


def get_spending_db():
    db = getattr(g, '_spendig_db', None)
    if db is None:
        flask_db = get_db()
        db = g._spendig_db = SpendingsDb()
        g._spendig_db.connect(flask_db)
    return db