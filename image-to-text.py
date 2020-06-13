import os

from PIL import Image
from pytesseract import image_to_string

print(image_to_string(Image.open(os.path.abspath('./files-imports/test.jpg')), lang='por'))
