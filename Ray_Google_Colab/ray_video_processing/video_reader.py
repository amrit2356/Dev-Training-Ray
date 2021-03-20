import sys
import time
from queue import Queue
from threading import Thread

import cv2
import ray

from edisn_frame import EdisnFrame


@ray.remote
class VideoReader:

    initialized = False
    enable_logging = False

    def __init__(self, video_path, enable_logging=False, queue_size=32):
        self.stream = cv2.VideoCapture(video_path)
        self.q = Queue(maxsize=queue_size)
        self.enable_logging = enable_logging
        self.initialized = True
        self.frame_number = 1
        self.complete = False

    def start(self):
        t = Thread(target=self.__read_frames, args=())
        t.daemon = True
        t.start()

    def __log(self, message):
        if self.enable_logging:
            print('[VideoReader] {}'.format(message))

    def __read_frames(self):

        self.__log('Started reading frames from video')

        while True:

            if not self.q.full():

                grabbed, frame = self.stream.read()

                if not grabbed:
                    self.__log('Read last frame')
                    self.q.put(None)
                    self.stream.release()
                    self.complete = True
                    break

                else:
                    self.__log('Read frame {}'.format(self.frame_number))
                    edisn_frame = EdisnFrame()

                    edisn_frame.frame_number = self.frame_number
                    edisn_frame.process_start_time = time.time()
                    edisn_frame.frame_bgr = frame

                    edisn_frame_plasma = ray.put(edisn_frame)
                    del edisn_frame

                    self.q.put(edisn_frame_plasma)
                    del edisn_frame_plasma

                    self.frame_number += 1

            else:
                self.__log('Queue full. Sleeping for 1ms')
                time.sleep(0.001)

    def more(self):
        return not self.q.empty()

    def read(self):
        return self.q.get()

    def get_video_details(self):

        if not self.initialized:
            raise Exception()

        width = int(self.stream.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = self.stream.get(cv2.CAP_PROP_FPS)
        frame_count = int(self.stream.get(cv2.CAP_PROP_FRAME_COUNT))

        return width, height, fps, frame_count
