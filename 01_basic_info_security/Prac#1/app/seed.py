import sys
import os
import random

# Добавим родительскую папку проекта в sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.extensions import db
from app.models import User, Book, Comment

users_data = [
    {"username": "nikifor", "password": "cm#8PGyQ"},
    {"username": "nazar", "password": "ps#d0Muc"},
    {"username": "ernest", "password": "L!0s*LiJ"},
    {"username": "agap", "password": ")3tnSFjr"},
    {"username": "alla", "password": "%n7kiAgv"},
    {"username": "daniil", "password": "Z3mjkd@p"},
    {"username": "elena", "password": "qY7*pm9!"},
    {"username": "zinaida", "password": "V@rp0sxQ"},
    {"username": "ivan", "password": "sJ3$kdw#"},
    {"username": "ksenia", "password": "Wz8@1lQr"},
]

books_data =  [
            {
                "title": "1984",
                "author": "Джордж Оруэлл",
                "cover_url": "https://covers.openlibrary.org/b/id/7222246-L.jpg"
            },
            {
                "title": "Убить пересмешника",
                "author": "Харпер Ли",
                "cover_url": "https://covers.openlibrary.org/b/id/8225261-L.jpg"
            },
            {
                "title": "Великий Гэтсби",
                "author": "Фрэнсис Скотт Фицджеральд",
                "cover_url": "https://covers.openlibrary.org/b/id/7352160-L.jpg"
            },
            {
                "title": "Гордость и предубеждение",
                "author": "Джейн Остин",
                "cover_url": "https://covers.openlibrary.org/b/id/8091016-L.jpg"
            },
            {
                "title": "Моби Дик",
                "author": "Герман Мелвилл",
                "cover_url": "https://covers.openlibrary.org/b/id/5551036-L.jpg"
            },
            {
                "title": "Война и мир",
                "author": "Лев Толстой",
                "cover_url": "https://covers.openlibrary.org/b/id/6979861-L.jpg"
            },
            {
                "title": "Над пропастью во ржи",
                "author": "Джером Дэвид Сэлинджер",
                "cover_url": "https://covers.openlibrary.org/b/id/8231856-L.jpg"
            },
        ]

comments_texts = [
    "Очень понравилась книга! Рекомендую!",
    "Глубокий сюжет и интересные персонажи.",
    "Ожидал большего, но всё равно неплохо.",
    "Отличное произведение, затягивает с первых страниц.",
    "Классика, которую стоит перечитать.",
    "Чтение далось тяжело, но в итоге не пожалел.",
    "Персонажи прописаны очень живо и реалистично.",
    "Философская глубина книги впечатляет.",
    "Потрясающий язык и стиль автора.",
    "Эта книга изменила мой взгляд на жизнь.",
    "Хочу прочитать ещё раз, очень зацепило.",
    "Иногда скучновато, но концовка всё оправдала.",
    "Советую всем поклонникам русской классики.",
    "История и атмосфера завораживают.",
]

def seed():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

        users = [User(**data) for data in users_data]
        db.session.add_all(users)
        db.session.commit()

        books = [Book(**data) for data in books_data]
        db.session.add_all(books)
        db.session.commit()

        for book in books:
            for _ in range(2):  # Можно увеличить при желании
                user = random.choice(users)
                content = random.choice(comments_texts)
                db.session.add(Comment(user_id=user.id, book_id=book.id, content=content))

        db.session.commit()
        print(f"✅ Seed завершён: {len(users)} пользователей, {len(books)} книг, {len(books) * 2} комментариев.")

if __name__ == '__main__':
    seed()
