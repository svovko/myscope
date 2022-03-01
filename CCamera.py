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

        # camera settings
        self.c_rotation = 90
        self.c_iso = 100
        self.c_sensor_mode = 3
        self.c_resolution = (1280, 720)
        self.c_exposure_mode = 'off' # možnost je še: 'night'
        #self.c_framerate = Fraction(1, 6)

    def start_streaming(self):
        print('Opening camera ...')
        self.camera             = picamera.PiCamera()
        self.camera.rotation    = self.c_rotation
        self.camera.iso         = self.c_iso # pravijo, da bi dal tole na 800 for maximum gain
        #self.camera.sensor_mode = self.c_sensor_mode
        self.camera.resolution  = self.c_resolution
        # probejmo tole spodaj:
        #self.camera.shutter_speed = 6000000
        #self.camera.framerate = self.c_framerate
        #self.camera.exposure_mode = self.c_exposure_mode
        time.sleep(5)

        self.thread = threading.Thread(target=self.start_stream)
        self.thread.start()


    def get_frame(self):
        return self.frame


    def get_picture(self):
        current = time.localtime()
        fname = '{}_{}_{}__{}_{}_{}.jpg'.format(current.tm_mday, current.tm_mon, current.tm_year,
                                                current.tm_hour, current.tm_min, current.tm_sec)

        # self.camera.resolution = (640, 480)
        # self.camera.shutter_speed = 6000000
        # self.camera.framerate = Fraction(1, 6)
        # time.sleep(3)
        # self.camera.exposure_mode = 'off'
        self.camera.capture('static/pictures/'+fname, use_video_port=False)

        #self.camera.shutter_speed = 0
        #self.camera.framerate = 30 # mogoče zaradi tega potem slike tako svetle???
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
            print('Camera closed!')

    def set_iso(self, iso):
        self.quit()
        self.c_iso = iso
        time.sleep(1)
        self.start_streaming()

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
