from flask import Blueprint, render_template
from app.models import Book, Comment  # <- Добавили импорт Comment
from app.extensions import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    books = Book.query.options(
        db.joinedload(Book.comments),                      # загружаем комментарии к книге
        db.joinedload(Book.comments).joinedload(Comment.user)  # загружаем пользователя из комментариев
    ).all()
    return render_template('main/index.html', books=books)

@main_bp.route('/practice')
def practice():
    return render_template('main/practice.html')

@main_bp.route('/book/<int:book_id>')
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template('main/book_detail.html', book=book)
