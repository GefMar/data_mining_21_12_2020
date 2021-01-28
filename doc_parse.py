import re
import PyPDF2
from PyPDF2.utils import PdfReadError
from pathlib import Path
from PIL import Image
import pytesseract


image_path = Path(__file__).parent.joinpath('images')


def pdf_image_extract(pdf_path: Path) -> list[Path]:
    file_decode = {
        '/DCTDecode': 'jpg',
        '/FlateDecode': 'png',
        '/JPXDecode': 'jp2'
    }
    results = []
    with pdf_path.open('rb') as file:
        try:
            pdf_file = PyPDF2.PdfFileReader(file)
        except PdfReadError:
            # обработка ошибки и запись в БД о ошибке
            pass
        for page_num, page in enumerate(pdf_file.pages):
            filename = f'{pdf_path.name}.{page_num}'
            img_data = page['/Resources']['/XObject']['/Im0']._data
            img_path = image_path.joinpath(filename)
            img_path.write_bytes(img_data)
            results.append(img_path)
        return results

def get_serial_number(image_path: Path) -> list[str]:
    numbers = []
    pattern = re.compile(r'(заводской.*номер)')
    image = Image.open(image_path)
    text_rus = pytesseract.image_to_string(image, 'rus')
    matchs = len(re.findall(pattern, text_rus))
    if not matchs:
        return numbers
    text_eng = pytesseract.image_to_string(image, 'eng')
    for idx, line in enumerate(text_rus.split('\n')):
        if re.match(pattern, line):
            number = text_eng.split('\n')[idx].split()[-1]
            numbers.append(number)
        if len(numbers) == matchs:
            break
    print(1)
    
    return numbers

if __name__ == '__main__':
    pdf_path = Path(__file__).parent.joinpath('8416_4.pdf')
    images = pdf_image_extract(pdf_path)
    numbers_gen = list(map(get_serial_number, images))
    print(1)
