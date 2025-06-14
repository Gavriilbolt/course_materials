from flask import Flask, request, render_template, abort, send_from_directory, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # Для flash-сообщений

# Directory where logs are stored
BASE_DIR = os.path.dirname(__file__)
LOG_DIR = os.path.join(BASE_DIR, 'logs')

@app.route('/')
def index():
    # Собираем список логов
    files = [f for f in os.listdir(LOG_DIR) if os.path.isfile(os.path.join(LOG_DIR, f))]
    return render_template('index.html', logs=files)

# Vulnerable to Path Traversal via the `filename` parameter
@app.route('/view_log')
def view_log():
    filename = request.args.get('filename', '')
    # Unsafe join, allows traversal
    filepath = os.path.join(LOG_DIR, filename)
    if not os.path.isfile(filepath):
        abort(404)
    with open(filepath, 'r', encoding="UTF8") as f:
        content = f.read()
    return render_template('logs.html', content=content, filename=filename)

# Vulnerable to arbitrary code execution via eval()
@app.route('/calculate', methods=['GET', 'POST'])
def calculate():
    result = None
    expr = ''
    if request.method == 'POST':
        expr = request.form.get('expr', '')
        try:
            result = eval(expr)  # Опасный eval
        except Exception as e:
            flash(f'Ошибка: {e}', 'danger')
            return redirect(url_for('calculate'))
    return render_template('calculate.html', result=result, expr=expr)

# Маршрут для описания задания
@app.route('/assignment')
def assignment():
    return render_template('assignment.html')

# Статические файлы
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(os.path.join(BASE_DIR, 'static'), filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)