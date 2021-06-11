import time
import io
import threading
import picamera
from fractions import Fraction


class Camera:

    def __init__(self):
        self.thread = None
        self.frame = None
        self.camera = None

        self.streaming = False

        # TODO - camera settings

    def start_streaming(self):
        self.camera = picamera.PiCamera()
        # self.camera.image_effect = 'colorswap'
        self.camera.rotation = 90
        self.camera.iso = 100
        self.camera.sensor_mode = 3
        self.camera.resolution = (640, 480)
        # self.camera.exposure_mode = 'night'

        self.thread = threading.Thread(target=self.start_stream)
        self.thread.start()

    def get_frame(self):
        return self.frame

    def get_picture(self):
        current = time.localtime()
        fname = '{}_{}_{}__{}_{}_{}.jpg'.format(current.tm_mday, current.tm_mon, current.tm_year,
                                                current.tm_hour, current.tm_min, current.tm_sec)

        self.camera.resolution = (640, 480)
        self.camera.shutter_speed = 5000000
        self.camera.framerate = Fraction(1, 5)
        time.sleep(3)
        self.camera.exposure_mode = 'off'
        self.camera.capture('static/pictures/'+fname, use_video_port=False)

        self.camera.resolution = (640, 480)
        self.camera.shutter_speed = 0
        self.camera.framerate = 30
        return fname

    #def stop_streaming(self):
    #    self.streaming = False
    #    if self.thread is not None:
    #        self.thread.join()

    def quit(self):
        self.streaming = False

        print('Waiting for thread ...')
        if self.thread is not None:
            self.thread.join()

        print('Closing camera ... ')
        if self.camera is not None:
            self.camera.close()

    def set_iso(self, iso):
        #self.quit()
        self.camera.iso = iso
        time.sleep(1)
        #self.start_streaming()

    # def set_exp(self, exp):  # read the docs!!!!
    #
    #     if exp == 0:
    #         self.camera.shutter_speed = 0
    #         self.camera.framerate = 0
    #     else:
    #         self.camera.shutter_speed = exp * 1000000
    #         self.camera.framerate = Fraction(1, exp)
    #
    #     self.camera.exposure_mode = 'off'

    def start_stream(self):
        self.streaming = True
        stream = io.BytesIO()

        for _ in self.camera.capture_continuous(stream, 'jpeg', use_video_port=True):
            stream.seek(0)
            self.frame = stream.read()
            stream.seek(0)
            stream.truncate()

            if not self.streaming:
                self.camera.close()
                break
