import argparse
import cv2 as cv
import os
import pyglet
import time
from video_converter import VideoConverter

def get_video_from_file(file_path):
    video = cv.VideoCapture(file_path)
    if (video.isOpened() == False):
        raise Exception("Error opening file")
    
    return video

def play(frames, fps):
    delay = 1 / fps
    next_frame_time = time.perf_counter() + delay
    
    for frame in frames:
        wait_time = next_frame_time - time.perf_counter()
        if (wait_time > 0):
            time.sleep(wait_time)
            
        next_frame_time += delay
        
        print(chr(27) + "[2J")
        print(frame)
        
def video_to_ascii(file_name):
    dir = os.getcwd() + "/input"
    file_path = dir + file_name
    
    video = get_video_from_file(file_path)
    fps = video.get(cv.CAP_PROP_FPS)
    print("Video fps: " + str(fps))
    
    start = time.perf_counter()
    ascii_video = VideoConverter().convert(video)
    end = time.perf_counter()
    print(f'Video converted in {round(end-start, 2)} second(s)')
    
    player = pyglet.media.Player()
    MediaLoad = pyglet.media.load(file_path)
    player.queue(MediaLoad)

    input("Press Enter to play")
    player.play()
    play(ascii_video, fps)
    print("END")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file")
    args = parser.parse_args()
    
    if args.file:
        video_to_ascii(args.file)

if __name__ == '__main__':
    main()
