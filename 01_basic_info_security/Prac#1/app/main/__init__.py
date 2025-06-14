from flask import Blueprint, render_template
from app.models import Book  # если у тебя модель Book уже определена

main = Blueprint('main', __name__)

@main.route('/')
def index():
    books = Book.query.all()
    return render_template('main/index.html', books=books)

@main.route('/practice')
def practice():
    return render_template('main/practice.html')
