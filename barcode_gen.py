from barcode import EAN13, EAN8, Code39

def make_barcode(code):
    number = str(code)
    
    # Выбор штрихкода в зависимости от длины кода
    if len(number) == 13:
        my_code = EAN13(number)
    elif len(number) == 8:
        my_code = EAN8(number)
    else:
        my_code = Code39(number, add_checksum=False)
    
    path = f"static/images/temp_ucp/{code}"
    my_code.save(path)
    return path
