import json
import os
import time
from os import path
from os.path import join
from queue import Queue
from threading import Thread


class JsonWriter():

    complete = False
    enable_logging = False

    def __init__(self, enable_logging=True, queue_size=8):
        self.q = Queue(maxsize=queue_size)
        self.enable_logging = enable_logging
        self.json = {}
        self.json_path = join(os.getcwd(), 'output.json')

        if path.exists(self.json_path):
            os.unlink(self.json_path)

        self.complete = False

    def start(self):
        t = Thread(target=self.__process_frames, args=())
        t.daemon = True
        t.start()

    def __log(self, message):
        if self.enable_logging:
            print('[JsonWriter] {}'.format(message))

    def __process_frames(self):

        self.__log('Started processing frames')

        while not self.complete:

            if not self.q.empty():

                edisn_frame = self.q.get()

                if type(edisn_frame) is type(None):
                    self.__log('Processed last frame')
                    self.__dump()
                    self.complete = True
                    return

                else:
                    self.__log('Processing frame {}'.format(edisn_frame.frame_number))

                    self.json[edisn_frame.frame_number] = {
                        'frame_number': edisn_frame.frame_number,
                        'process_start_time': edisn_frame.process_start_time,
                        'process_end_time': edisn_frame.process_end_time,
                        'rgb_start_time': edisn_frame.rgb_start_time,
                        'rgb_end_time': edisn_frame.rgb_end_time,
                        'resize_start_time': edisn_frame.resize_start_time,
                        'resize_end_time': edisn_frame.resize_end_time,
                        'grayscale_start_time': edisn_frame.grayscale_start_time,
                        'grayscale_end_time': edisn_frame.grayscale_end_time,
                        'disk_write_start_time': edisn_frame.disk_write_start_time,
                        'disk_write_end_time': edisn_frame.disk_write_end_time,
                    }

                    if edisn_frame.frame_number % 100 == 0:
                        self.__dump()

                    del edisn_frame

            else:
                # self.__log('Queue empty. Sleeping for 1ms')
                time.sleep(0.001)

    def __dump(self):
        with open(self.json_path, 'w') as f:
            json.dump(self.json, f, indent=4)

    def process_frame(self, edisn_frame):
        if not self.q.full():
            self.q.put(edisn_frame)

    def more(self):
        return self.complete is False

    def destroy(self):
        while not self.complete:
            time.sleep(50)
        
        self.__log('Destroyed!')
