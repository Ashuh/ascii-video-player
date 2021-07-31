import cv2 as cv
import imutils
import math

class ImageConverter:
    def __init__(self):
        palette = [' ', '.', ':', '-', '=', '+', '*', '#', '%', '@']
        self.mapping = list()
        step = 255 / len(palette)
        palette_index = 0
        cur_max = math.ceil(step)
        
        for i in range(0,256):
            if i >= cur_max:
                palette_index += 1
                cur_max = math.ceil(cur_max + step)
            self.mapping.append(palette[palette_index])

    def grayscale_to_ascii(self, img):
        ascii = str()
        rows, cols = img.shape

        for i in range(rows):
            for j in range(cols):
                brightness = img[i, j]
                ascii += self.mapping[brightness] + ' '
            ascii += '\n'

        ascii = ascii[:-1]
        return ascii

    def convert(self, img):
        resize = imutils.resize(img, width=100)
        gray = cv.cvtColor(resize, cv.COLOR_BGR2GRAY)
        ascii_str = self.grayscale_to_ascii(gray)

        return ascii_str
        