import time
from queue import Queue
from threading import Thread

import ray

from grayscale_converter import GrayscaleConverter
from helper import resize_image


@ray.remote
class FrameResizer:

    complete = False
    enable_logging = False

    def __init__(self, enable_logging=False, queue_size=8):
        self.q = Queue(maxsize=queue_size)
        self.enable_logging = enable_logging
        self.grayscale_converter = GrayscaleConverter.remote(enable_logging=True)
        self.grayscale_converter.start.remote()
        time.sleep(0.1)

    def start(self):
        t = Thread(target=self.__process_frames, args=())
        t.daemon = True
        t.start()

    def __log(self, message):
        if self.enable_logging:
            print('[FrameResizer] {}'.format(message))

    def __process_frames(self):

        self.__log('Started processing frames')

        while not self.complete:

            if not self.q.empty():

                edisn_frame = self.q.get()

                if type(edisn_frame) is type(None):
                    self.__log('Processed last frame')
                    ray.get(self.grayscale_converter.process_frame.remote(ray.put(edisn_frame)))
                    # self.grayscale_converter.process_frame(edisn_frame)
                    self.complete = True
                    del edisn_frame

                else:
                    self.__log('Processing frame {}'.format(edisn_frame.frame_number))

                    edisn_frame.resize_start_time = time.time()
                    edisn_frame.frame_resized = resize_image(edisn_frame.frame_rgb)
                    edisn_frame.resize_end_time = time.time()

                    ray.get(self.grayscale_converter.process_frame.remote(ray.put(edisn_frame)))
                    # self.grayscale_converter.process_frame(edisn_frame)
                    del edisn_frame

            else:
                # self.__log('Queue empty. Sleeping for 1ms')
                time.sleep(0.001)

    def process_frame(self, edisn_frame):
        if type(edisn_frame) is not type(None):
            self.__log('Recevied frame {}'.format(edisn_frame.frame_number))

        else:
            self.__log('Received last frame')

        # self.__log('Queue size: {}'.format(self.q.qsize()))
        self.q.put(edisn_frame)
        del edisn_frame

    def more(self):
        return not self.complete

    def destroy(self):
        while not self.q.empty():
            ray.get(self.grayscale_converter.more.remote())
            time.sleep(0.05)
        
        self.__log('Calling destroy from Grayscale Converter!')
        message = ray.get(self.grayscale_converter.destroy.remote())
        self.__log(message)
        time.sleep(0.1)
        return message