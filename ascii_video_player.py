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
        
def play(frames, fps, output):
    delay = 1 / fps
    next_frame_time = time.perf_counter() + delay

    for frame in frames:
        wait_time = next_frame_time - time.perf_counter()
        
        if (wait_time > 0):
            if output == "string":
                time.sleep(wait_time)
                print(chr(27) + "[2J")
                print(frame)
            elif output == "image": 
                cv.waitKey(int(wait_time * 1000))
                cv.imshow("Video", frame)

        next_frame_time += delay
        
def video_to_ascii(file_name, output, width = 100):
    dir = os.getcwd() + "/input"
    file_path = dir + file_name
    
    video = get_video_from_file(file_path)
    fps = video.get(cv.CAP_PROP_FPS)
    print("Video fps: " + str(fps))
    
    start = time.perf_counter()
    ascii_video = VideoConverter().convert(video, output, width)
    end = time.perf_counter()
    print(f'Video converted in {round(end-start, 2)} second(s)')
    
    player = pyglet.media.Player()
    MediaLoad = pyglet.media.load(file_path)
    player.queue(MediaLoad)

    input("Press Enter to play")
    player.play()
    play(ascii_video, fps, output)
    print("END")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file")
    parser.add_argument("-o", "--output")
    parser.add_argument("-w", "--width")
    args = parser.parse_args()
    
    if args.file and args.output:
        if args.width:
            video_to_ascii(args.file, args.output, int(args.width))
        else:
            video_to_ascii(args.file, args.output)

if __name__ == '__main__':
    main()
