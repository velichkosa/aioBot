import pytesseract
import cv2


def recognition(src, image_name):
    # функция распознавания текста с картинки
    image = cv2.imread(src + image_name)
    return pytesseract.image_to_string(image, lang='rus+eng')
