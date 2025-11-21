from datetime import datetime
from dataclasses import dataclass

@dataclass
class Post:
    title: str
    content: str
    created_at: datetime
    is_published: bool