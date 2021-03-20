import time
from queue import Queue
from threading import Thread

import ray

from frame_resizer import FrameResizer
from helper import convert_to_rgb


@ray.remote
class RGBConverter:

    complete = False
    enable_logging = False

    def __init__(self, enable_logging=True, queue_size=8):
        self.q = Queue(maxsize=queue_size)
        self.enable_logging = enable_logging
        self.frame_resizer = FrameResizer.remote(enable_logging=True)
        self.frame_resizer.start.remote()
        time.sleep(0.1)

    def start(self):
        t = Thread(target=self.__process_frames, args=())
        t.daemon = True
        t.start()

    def __log(self, message):
        if self.enable_logging:
            print('[RGBConverter] {}'.format(message))

    def __process_frames(self):

        self.__log('Started processing frames')

        while not self.complete:

            if not self.q.empty():

                edisn_frame = self.q.get()

                if type(edisn_frame) is type(None):
                    self.__log('Processed last frame')
                    ray.get(self.frame_resizer.process_frame.remote(ray.put(edisn_frame)))
                    # self.frame_resizer.process_frame(edisn_frame)
                    self.complete = True
                    del edisn_frame

                else:
                    self.__log('Processing frame {}'.format(edisn_frame.frame_number))

                    edisn_frame.rgb_start_time = time.time()
                    edisn_frame.frame_rgb = convert_to_rgb(edisn_frame.frame_bgr)
                    edisn_frame.rgb_end_time = time.time()

                    ray.get(self.frame_resizer.process_frame.remote(ray.put(edisn_frame)))
                    # self.frame_resizer.process_frame(edisn_frame)
                    del edisn_frame

            else:
                #self.__log('Queue empty. Sleeping for 1ms')
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
            ray.get(self.frame_resizer.more.remote())
            time.sleep(0.05)
        
        # self.__log('Destroyed!')
        self.__log('Calling destroy from frame resizer!')
        message = ray.get(self.frame_resizer.destroy.remote())
        self.__log(message)
        time.sleep(0.1)
        return True
        
