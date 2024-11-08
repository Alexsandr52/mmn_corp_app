from flask import Flask, render_template, request
import barcode_gen

app = Flask(__name__)

@app.route('/')
def index():
    # Передаем данные в шаблон
    return render_template('index.html')

@app.route('/save_barcode', methods=['POST'])
def save_barcode():
    barcode = request.form.get('barcode')
    tag = request.form.get('tag')

    barcode_path = None
    if len(str(barcode)) == 12:
        barcode_path = barcode_gen.make_barcode(barcode)
        print(f"Generated barcode path: {barcode_path}")

    # Проверим, что путь не пустой, и добавим расширение
    return render_template(
        'index.html',
        message="Изменения сохранены!",
        barcode_path=f'{barcode_path}.svg' if barcode_path else None
    )

@app.route('/static/<path:path>')
def send_static(path):
    return app.send_static_file(path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
