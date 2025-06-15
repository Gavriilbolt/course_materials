
from flask import Blueprint, request, render_template, redirect, url_for, abort, flash
from ..extensions import db
from ..models import User, Book, Comment
from sqlalchemy import text


admin_bp = Blueprint('admin', __name__, url_prefix='/admin', template_folder='templates')


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        sql = text(f"""
            SELECT id, username, password FROM users
            WHERE username = '{username}' AND password = '{password}'
        """)
        users = db.session.execute(sql).fetchall()
        
        
        if users:
            return redirect(url_for('admin.dashboard'))
        else:
            return render_template('admin/login.html', error='Неверный логин или пароль')
    return render_template('admin/login.html')


@admin_bp.route('/dashboard')
def dashboard():
    return render_template('admin/dashboard.html')


@admin_bp.route('/users')
def users():
    users = User.query.all()
    return render_template('admin/users.html', users=users)


@admin_bp.route('/books')
def books():
    books = Book.query.all()
    return render_template('admin/books.html', books=books)


@admin_bp.route('/books/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        cover_url = request.form.get('cover_url') or None

        if title and author:
            new_book = Book(title=title, author=author, cover_url=cover_url)
            db.session.add(new_book)
            db.session.commit()
            return redirect(url_for('admin.books'))
        else:
            flash('Поля "Название" и "Автор" обязательны.')
    return render_template('admin/add_book.html')


@admin_bp.route('/comments')
def comments():
    comments = Comment.query.join(Book).outerjoin(User).all()
    return render_template('admin/comments.html', comments=comments)


@admin_bp.route('/comments/delete/<int:comment_id>', methods=['POST'])
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('admin.comments'))
