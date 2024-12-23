from typing import Dict, Any

class UserType:
    id: int
    username: str
    password: str

class ArticleType:
    id: int
    title: str
    content: str
    author_id: int

def user_response(user: UserType) -> Dict[str, Any]:
    return {
        "id": user.id,
        "username": user.username
    }

def article_response(article: ArticleType) -> Dict[str, Any]:
    return {
        "id": article.id,
        "title": article.title,
        "content": article.content,
        "author_id": article.author_id
    }