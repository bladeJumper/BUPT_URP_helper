from PIL import Image,ImageEnhance
import pytesseract

#验证码识别
def image_to_str(path):
    image = Image.open(path)
    image = image.convert('L')
    sharpness =ImageEnhance.Contrast(image)
    image = sharpness.enhance(2.0)
    vcode = pytesseract.image_to_string(image)
    return vcode