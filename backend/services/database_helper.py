import psycopg2
from psycopg2 import extras


class DatabaseHelper:
    DB_NAME = 'ips_flask'
    USER = 'postgres'
    HOST = 'localhost'

    @classmethod
    def connect(cls):
        return psycopg2.connect(
            dbname=cls.DB_NAME,
            user=cls.USER,
            host=cls.HOST
        )

    @classmethod
    def insert(cls, table, model):
        with cls.connect() as conn:
            with conn.cursor() as cur:
                data = {key: value for key, value in model.__dict__.items() if value is not None and key != 'id'}
                columns = ', '.join(data.keys())
                placeholders = ', '.join(f'%s' for _ in data.values())
                sql = f'INSERT INTO {table} ({columns}) VALUES ({placeholders})'
                cur.execute(sql, tuple(data.values()))
                conn.commit()

    @classmethod
    def delete(cls, table, model):
        with cls.connect() as conn:
            with conn.cursor() as cur:
                sql = f'DELETE FROM {table} WHERE id = %s'
                cur.execute(sql, (model.id,))
                conn.commit()

    @classmethod
    def update(cls, table, model):
        with cls.connect() as conn:
            with conn.cursor() as cur:
                assignments = ', '.join(f'{key} = %s' for key in model.__dict__.keys())
                sql = f'UPDATE {table} SET {assignments} WHERE id = %s'
                values = list(model.__dict__.values()) + [model.id]
                cur.execute(sql, values)
                conn.commit()

    @classmethod
    def find_by_name(cls, table, name):
        with cls.connect() as conn:
            with conn.cursor(cursor_factory=extras.DictCursor) as cur:
                sql = f'SELECT * FROM {table} WHERE name = %s'
                cur.execute(sql, (name,))
                result = cur.fetchone()
                return result
            
    @classmethod
    def find_by_id(cls, table, id):
        with cls.connect() as conn:
            with conn.cursor(cursor_factory=extras.DictCursor) as cur:
                sql = f'SELECT * FROM {table} WHERE id = %s'
                cur.execute(sql, (id,))
                result = cur.fetchone()
                return result
            
    @classmethod
    def find_all(cls, table):
        with cls.connect() as conn:
            with conn.cursor(cursor_factory=extras.DictCursor) as cur:
                sql = f'SELECT * FROM {table}'
                cur.execute(sql)
                result = cur.fetchall()
                return result