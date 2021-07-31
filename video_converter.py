import concurrent.futures
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
        
    def convert(self, video):
        frames = self.extract_frames(video)
        print(str(len(frames)) + " frames extracted")

        ascii_frames = list()
        with concurrent.futures.ProcessPoolExecutor() as executor:
            results = executor.map(self.image_converter.convert, frames)
            for res in results:
                ascii_frames.append(res)
        
        return ascii_frames
