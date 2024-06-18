from backend.app.services.database_helper import DatabaseHelper
from werkzeug.security import check_password_hash

class User:
    def __init__(self, id=None, name=None, password=None):
        self.id = id
        self.name = name
        self.password = password

    def save(self):
        if self.id is None:
            # 新規作成の場合
            DatabaseHelper.insert('users', self)
        else:
            # 既存のユーザーの更新
            DatabaseHelper.update('users', self)

    def delete(self):
        if self.id is not None:
            DatabaseHelper.delete('users', self)

    @staticmethod
    def find_by_name(name):
        result = DatabaseHelper.find_by_name('users', name)
        if result:
            return User(id=result['id'], name=result['name'], password=result['password'])
        return None
    
    @staticmethod
    def find_by_id(id):
        result = DatabaseHelper.find_by_id('users', id)
        if result:
            return User(id=result['id'], name=result['name'], password=result['password'])
        return None
    
    @staticmethod
    def find_all():
        results = DatabaseHelper.find_all('users')
        for result in results:
            yield User(id=result['id'], name=result['name'], password=result['password'])


    def check_password(self, password):
        return check_password_hash(self.password,password)