from flask import Blueprint, request, render_template, redirect, url_for, abort
from ..extensions import db
from sqlalchemy import text

comments_bp = Blueprint('comments', __name__, url_prefix='/comments')

@comments_bp.route('/', methods=['GET'])
def list_comments():
    sql = text(
        "SELECT c.id, u.username, c.content, b.title AS book_title "
        "FROM comments c "
        "JOIN users u ON c.user_id = u.id "
        "JOIN books b ON c.book_id = b.id"
    )
    comments = db.session.execute(sql).fetchall()
    return render_template('comments/list.html', comments=comments)

@comments_bp.route('/add', methods=['GET', 'POST'])
def add_comment():
    if request.method == 'POST':
        username = request.form.get('username', '')
        content = request.form.get('content', '')
        book_id = request.form.get('book_id', '')

        sql = text(
            f"INSERT INTO comments (user_id, book_id, content) VALUES ("
            f"(SELECT id FROM users WHERE username = '{username}'), {book_id}, '{content}')"
        )
        try:
            db.session.execute(sql)
            db.session.commit()
            return redirect(url_for('comments.list_comments'))
        except Exception as e:
            print(f"Ошибка при добавлении комментария: {e}")
            db.session.rollback()
            abort(400)

    # 📘 Получаем список книг для выпадающего списка
    books = db.session.execute(text("SELECT id, title FROM books")).fetchall()
    return render_template('comments/add.html', books=books)

