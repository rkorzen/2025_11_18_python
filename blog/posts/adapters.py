from abc import ABC, abstractmethod
from .dto import Post
from .models import Post as DjangoPost
from django.utils import timezone


class DatabaseAdapter(ABC):

    @abstractmethod
    def get_posts(self):
        ...


class FakeDatabaseAdapter(DatabaseAdapter):
    def get_posts(self):
        return [
            Post(
                title="Post 1", content="Post 1 content", created_at=timezone.now(), is_published=True
            ),
            Post(
                title="Post 2", content="Post 2 content", created_at=timezone.now(), is_published=True
            )
        ]


class DjangoAdapter(DatabaseAdapter):

    def get_posts(self):
        return DjangoPost.objects.all()
