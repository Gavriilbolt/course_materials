import sys
import os

# Добавляем корневую папку проекта в PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app

app = create_app()

if __name__ == "__main__":
    # В Docker нужно слушать на 0.0.0.0, иначе Flask недоступен снаружи
    app.run(host='0.0.0.0', port=5000, debug=True)
