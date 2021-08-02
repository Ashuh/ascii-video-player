import cv2 as cv
import imutils
import math
import numpy as np

class ImageConverter:
    def __init__(self):
        palette = [' ', '.', ':', '-', '=', '+', '*', '#', '%', '@']
        self.mapping = list()
        step = 255 / len(palette)
        palette_index = 0
        cur_max = math.ceil(step)

        for i in range(0, 256):
            if i >= cur_max:
                palette_index += 1
                cur_max = math.ceil(cur_max + step)
            self.mapping.append(palette[palette_index])

    def grayscale_to_ascii(self, img):
        ascii = list()
        rows, cols = img.shape

        for i in range(rows):
            row = list()
            for j in range(cols):
                row.append(self.mapping[img[i, j]])
            ascii.append(row)

        return ascii

    def ascii_to_str(self, ascii_arr):
        string = str()

        for row in ascii_arr:
            for char in row:
                string += char + ' '
            string += '\n'

        return string

    def ascii_to_img(self, ascii_arr):
        cell_size = 16
        font = cv.FONT_HERSHEY_COMPLEX
        fontScale = 0.5
        thickness = 1
        color = (255, 255, 255)

        output = np.zeros(0)

        for row in ascii_arr:
            row_cells = np.zeros(0)

            for char in row:
                cell = np.zeros((cell_size, cell_size, 1), dtype="uint8")
                textsize = cv.getTextSize(char, font, fontScale, thickness)[0]
                textX = (cell_size - textsize[0]) // 2
                textY = (cell_size + textsize[1]) // 2
                cell = cv.putText(cell, char, (textX, textY), font,
                                  fontScale, color, thickness, cv.LINE_AA)

                if len(row_cells) == 0:
                    row_cells = cell
                else:
                    row_cells = cv.hconcat([row_cells, cell])

            if len(output) == 0:
                output = row_cells
            else:
                output = cv.vconcat([output, row_cells])

        return output
    
    def convert(self, img, output, width = 100):
        resize = imutils.resize(img, width)
        gray = cv.cvtColor(resize, cv.COLOR_BGR2GRAY)
        ascii_arr = self.grayscale_to_ascii(gray)
        
        if output == "string":
            return self.ascii_to_str(ascii_arr)
        elif output == "image":
            return self.ascii_to_img(ascii_arr)
