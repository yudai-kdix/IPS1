from backend.app.services.database_helper import DatabaseHelper


class Face:
    def __init__(self, id=None, name=None, facevec=None, user_id=None,video_id=None):
        self.id = id
        self.name = name
        self.facevec = facevec
        self.user_id = user_id
        self.video_id = video_id

    def save(self):
        if self.id is None:
            # 新規作成の場合
            DatabaseHelper.insert('faces', self)
        else:
            # 既存のユーザーの更新
            DatabaseHelper.update('faces', self)

    def delete(self):
        if self.id is not None:
            DatabaseHelper.delete('faces', self)

    @staticmethod
    def find_by_name(name):
        result = DatabaseHelper.find_by_name('faces', name)
        if result:
            return Face(id=result['id'], name=result['name'], facevec=result['facevec'],user_id=result['user_id'],video_id=result['video_id'] )
        return None
    
    @staticmethod
    def find_by_id(id):
        result = DatabaseHelper.find_by_id('faces', id)
        if result:
            return Face(id=result['id'], name=result['name'], facevec=result['facevec'],user_id=result['user_id'],video_id=result['video_id'])
        return None
    
    @staticmethod
    def find_all():
        results = DatabaseHelper.find_all('faces')
        for result in results:
            yield Face(id=result['id'], name=result['name'], facevec=result['facevec'],user_id=result['user_id'],video_id=result['video_id'])