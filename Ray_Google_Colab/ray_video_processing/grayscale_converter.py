import time
from queue import Queue
from threading import Thread

import ray

from disk_writer import DiskWriter
from helper import convert_to_gray


@ray.remote
class GrayscaleConverter:

    complete = False
    enable_logging = False

    def __init__(self, enable_logging=False, queue_size=8):
        self.q = Queue(maxsize=queue_size)
        self.enable_logging = enable_logging
        self.disk_writer = DiskWriter.remote(enable_logging=True)
        self.disk_writer.start.remote()
        time.sleep(0.1)

    def start(self):
        t = Thread(target=self.__process_frames, args=())
        t.daemon = True
        t.start()

    def __log(self, message):
        if self.enable_logging:
            print('[GrayscaleConverter] {}'.format(message))

    def __process_frames(self):

        self.__log('Started processing frames')

        while not self.complete:

            if not self.q.empty():

                edisn_frame = self.q.get()

                if type(edisn_frame) is type(None):
                    self.__log('Processed last frame')
                    ray.get(self.disk_writer.process_frame.remote(ray.put(edisn_frame)))
                    self.complete = True
                    del edisn_frame

                else:
                    self.__log('Processing frame {}'.format(edisn_frame.frame_number))

                    edisn_frame.grayscale_start_time = time.time()
                    edisn_frame.frame_grayscale = convert_to_gray(edisn_frame.frame_resized)
                    edisn_frame.grayscale_end_time = time.time()

                    ray.get(self.disk_writer.process_frame.remote(ray.put(edisn_frame)))
                    #self.disk_writer.process_frame(edisn_frame)
                    del edisn_frame

            else:
                # self.__log('Queue empty. Sleeping for 1ms')
                time.sleep(0.001)

    def process_frame(self, edisn_frame):
        if type(edisn_frame) is not type(None):
            self.__log('Recevied frame {}'.format(edisn_frame.frame_number))

        else:
            self.__log('Received last frame')

        self.__log('Queue size: {}'.format(self.q.qsize()))
        self.q.put(edisn_frame)
        del edisn_frame

    def more(self):
        return not self.complete

    def destroy(self):
        while not self.q.empty():
            ray.get(self.disk_writer.more.remote())
            time.sleep(0.05)
        
        self.__log('Calling destroy from Disk Writer!')
        message = ray.get(self.disk_writer.destroy.remote())
        self.__log(message)
        time.sleep(0.1)
        return message
