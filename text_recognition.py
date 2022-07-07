import pytesseract
import cv2
from pyaspeller import YandexSpeller


# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def recognition(src, image_name, language):
    lang = []
    if language == 'en':
        lang = ['en', 'eng']
    elif language == 'ru':
        lang = ['ru', 'rus']

    # функция распознавания текста с картинки
    image = cv2.imread(src + image_name)

    speller = YandexSpeller(ignore_urls=True, ignore_digits=True, lang=lang[0])
    fixed = speller.spelled(pytesseract.image_to_string(image, lang=lang[1]))
    return fixed
