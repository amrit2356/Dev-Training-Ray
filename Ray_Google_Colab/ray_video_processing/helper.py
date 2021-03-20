import cv2
import time


def convert_to_rgb(img):
    time.sleep(0.02)
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def resize_image(img):
    time.sleep(0.03)
    return cv2.resize(img, (400, 400))


def convert_to_gray(img):
    time.sleep(0.04)
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)