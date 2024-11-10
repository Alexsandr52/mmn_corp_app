from flask import Flask, render_template, request, g
import barcode_gen
import sqlite3

app = Flask(__name__)
DATABASE = 'database.db'

# manage db defs
def get_db(DATABASE):
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # Это ключевая строка для возврата строк как словарей
    return db

def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

app.teardown_appcontext(close_connection)

def add_item(name, img_link):
    db = get_db(DATABASE)
    db.execute('INSERT INTO items (name, img_link) VALUES (?, ?)', (name, img_link))
    db.commit()

def init_db():
    with app.app_context():
        db = get_db(DATABASE)
        db.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                img_link TEXT NOT NULL
            );
        ''')
        db.commit()

def get_last_5_items():
    db = get_db(DATABASE)
    cursor = db.execute('SELECT * FROM items ORDER BY id DESC LIMIT 5')
    rows = cursor.fetchall()
    return [dict(row) for row in rows]  # Теперь строки могут быть преобразованы в словари

# app main logic
@app.route('/')
def index():
    items = get_last_5_items()  # Получаем последние 5 записей
    return render_template('index.html', items=items)

@app.route('/save_barcode', methods=['POST'])
def save_barcode():
    barcode = request.form.get('barcode')
    tag = request.form.get('tag')

    barcode_path = None
    if barcode:
        barcode_path = barcode_gen.make_barcode(barcode)
        print(f"Generated barcode path: {barcode_path}")

    if barcode_path:
        add_item(tag, f'{barcode_path}.svg')

    items = get_last_5_items()  # Получаем последние 5 записей для отображения

    return render_template(
        'index.html',
        message="Изменения сохранены!" if barcode_path else "Ошибка генерации штрихкода!",
        barcode_path=f'{barcode_path}.svg',  # передаем путь к штрихкоду
        items=items
    )

# setup and static
@app.route('/static/<path:path>')
def send_static(path):
    return app.send_static_file(path)

init_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
