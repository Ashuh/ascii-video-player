import concurrent.futures
import cv2 as cv
from image_converter import ImageConverter


class VideoConverter:
    def __init__(self):
        self.image_converter = ImageConverter()

    def extract_frames(self, video):
        frames = list()
        success, img = video.read()

        while success:
            frames.append(img)
            success, img = video.read()

        return frames

    def convert(self, video, output, width=100):
        frames_raw = self.extract_frames(video)
        print(str(len(frames_raw)) + " frames extracted")

        frames_ascii = list()

        with concurrent.futures.ProcessPoolExecutor() as executor:
            outputs = [output] * len(frames_raw)
            widths = [width] * len(frames_raw)

            results = executor.map(
                self.image_converter.convert, frames_raw, outputs, widths)
            for res in results:
                frames_ascii.append(res)

        return frames_ascii
