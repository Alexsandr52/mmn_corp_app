from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    # Передаем данные в шаблон, например, начальный выбор изображения
    return render_template('index.html')

@app.route('/save_barcode', methods=['POST'])
def save_barcode():
    # Получаем данные из формы модального окна
    barcode = request.form.get('barcode')
    tag = request.form.get('tag')

    # Вы можете сохранить эти данные в базе данных или использовать их дальше
    print(f"Barcode: {barcode}, Tag: {tag}")

    # Перенаправляем обратно на главную страницу
    return render_template('index.html', message="Изменения сохранены!")

@app.route('/static/<path:path>')
def send_static(path):
    return app.send_static_file(path)

if __name__ == '__main__':
    app.run(debug=True)
