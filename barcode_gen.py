from barcode import EAN13 

def make_barcode(code):
    number = str(code)
    my_code = EAN13(number)
    path = f"static/images/{code}"
    my_code.save(path)
    return path  # Возвращаем путь к изображению

