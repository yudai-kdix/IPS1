from backend.app.services.database_helper import DatabaseHelper


class Video:
    def __init__(self, id=None, name=None, path=None, user_id=None):
        self.id = id
        self.name = name
        self.path = path
        self.user_id = user_id


    def save(self):
        if self.id is None:
            # 新規作成の場合
            DatabaseHelper.insert('videos', self)
        else:
            # 既存のユーザーの更新
            DatabaseHelper.update('videos', self)

    def delete(self):
        if self.id is not None:
            DatabaseHelper.delete('videos', self)

    @staticmethod
    def find_by_name(name):
        result = DatabaseHelper.find_by_name('videos', name)
        if result:
            return Video(id=result['id'], name=result['name'], path=result['path'])
        return None
    
    @staticmethod
    def find_by_id(id):
        result = DatabaseHelper.find_by_id('videos', id)
        if result:
            return Video(id=result['id'], name=result['name'], path=result['path'])
        return None
    
    @staticmethod
    def find_by_user_id(user_id):
        results = DatabaseHelper.find_by_user_id('videos', user_id)
        for result in results:
            yield Video(id=result['id'], name=result['name'], path=result['path'], user_id=result['user_id'])
    @staticmethod
    def find_all():
        results = DatabaseHelper.find_all('videos')
        for result in results:
            yield Video(id=result['id'], name=result['name'], path=result['path'])