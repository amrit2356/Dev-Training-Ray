import argparse
import time

import ray

from rgb_converter import RGBConverter
from video_reader import VideoReader


def main(args):
    ray.init()
    frame_number = 1

    video_reader = VideoReader.remote(args.video_path)
    rgb_converter = RGBConverter.remote()

    width, height, fps, frame_count = ray.get(video_reader.get_video_details.remote())

    print('Video Details:')
    print('*************************')
    print('Width: {}'.format(width))
    print('Height: {}'.format(height))
    print('FPS: {}'.format(fps))
    print('Frame Count: {}'.format(frame_count))
    print('*************************')

    video_reader.start.remote()
    rgb_converter.start.remote()

    time.sleep(0.5)

    while ray.get(video_reader.more.remote()):

        print('Started processing frame number {}'.format(frame_number))

        edisn_frame = ray.get(video_reader.read.remote())
        ray.get(rgb_converter.process_frame.remote(edisn_frame))
        del edisn_frame

        frame_number += 1
        time.sleep(0.001)
    print("calling destroy from RGBConverter")
    flag = ray.get(rgb_converter.destroy.remote())
    if flag == True:
        print("Destroy Process Complete... Ray Shutdown")
    ray.shutdown()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--video_path', type=str, required=True)
    main(parser.parse_args())
