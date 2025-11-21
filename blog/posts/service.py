from .adapters import DatabaseAdapter

class PostService:

    def get_posts(self, db: DatabaseAdapter):
        return db.get_posts()
