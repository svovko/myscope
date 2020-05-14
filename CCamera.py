import time
import io
import threading
import picamera


class Camera:

    def __init__(self):
        self.thread = None
        self.frame = None
        self.camera = None

        self.streaming = False

        # TODO - camera settings

    def start_streaming(self):
        self.camera = picamera.PiCamera()
        self.thread = threading.Thread(target=self.start_stream)
        self.thread.start()

    def get_frame(self):
        return self.frame

    def get_picture(self):
        current = time.localtime()
        fname = '{}_{}_{}__{}_{}_{}.jpg'.format(current.tm_mday, current.tm_mon, current.tm_year,
                                                                current.tm_hour, current.tm_min, current.tm_sec)
        self.camera.capture('static/pictures/'+fname, use_video_port=False)
        return fname

    def stop_streaming(self):
        self.streaming = False

        print('Waiting for thread ...')
        if self.thread is not None:
            self.thread.join()

        print('Closing camera ... ')
        if self.camera is not None:
            self.camera.close()

    def start_stream(self):
        self.streaming = True
        stream = io.BytesIO()
        for _ in self.camera.capture_continuous(stream, 'jpeg', use_video_port=True):
            stream.seek(0)
            self.frame = stream.read()

            stream.seek(0)
            stream.truncate()

            if not self.streaming:
                break
