import os
import time
from os.path import join
from queue import Queue
from threading import Thread

import ray
import cv2
# from json_writer import JsonWriter

@ray.remote
class DiskWriter:

    complete = False
    enable_logging = False

    def __init__(self, enable_logging, queue_size=8):
        self.q = Queue(maxsize=queue_size)
        self.enable_logging = enable_logging
        # self.jsonwriter = JsonWriter()
        # self.jsonwriter.start()
        time.sleep(0.1)

    def start(self):
        t = Thread(target=self.__process_frames, args=())
        t.daemon = True
        t.start()

    def __log(self, message):
        if self.enable_logging:
            print('[DiskWriter] {}'.format(message))

    def __process_frames(self):

        self.__log('Started processing frames')

        while not self.complete:

            if not self.q.empty():

                edisn_frame = self.q.get()

                if type(edisn_frame) is type(None):
                    self.__log('Processed last frame')
                    #self.jsonwriter.process_frame(edisn_frame)
                    self.complete = True
                    del edisn_frame

                else:
                    self.__log('Processing frame {}'.format(edisn_frame.frame_number))

                    edisn_frame.disk_write_start_time = time.time()
                    cv2.imwrite(join(os.getcwd(), 'frames', '{}.jpg'.format(edisn_frame.frame_number)), edisn_frame.frame_grayscale)
                    edisn_frame.disk_write_end_time = time.time()
                    edisn_frame.process_end_time = time.time()

                    # self.jsonwriter.process_frame(edisn_frame)

            else:
                # self.__log('Queue empty. Sleeping for 1ms')
                time.sleep(0.001)

    def process_frame(self, edisn_frame):
        if type(edisn_frame) is not type(None):
            self.__log('Recevied frame {}'.format(edisn_frame.frame_number))

        else:
            self.__log('Received last frame')

        #self.__log('Queue size: {}'.format(self.q.qsize()))
        self.q.put(edisn_frame)
        del edisn_frame

    def more(self):
        return not self.complete

    def destroy(self):
        # self.jsonwriter.destroy()

        # while self.jsonwriter.more():
            # time.sleep(0.05)

        while not self.q.empty():
            time.sleep(0.05)

        self.__log('Destroyed!')
        time.sleep(0.05)
        return 'Destroyed!'
