import RPi.GPIO as gpio
from time import sleep
import CoordinateConversion
from LocationInfo import LocationInfo
import threading


class Telescope:

    def __init__(self, pd_t, pd_b, ps_t, ps_b):
        self.pin_dir_top = pd_t
        self.pin_dir_bottom = pd_b

        self.pin_stp_top = ps_t
        self.pin_stp_bottom = ps_b

        #  (1D = 60M = 3600s)
        self.dms_latitude = (45, 48)  # omiting seconds
        self.dms_longitude = (15, 10)  # omiting seconds

        self.initialized = False

        self.altitude_m = 0  # top angle in minutes
        self.azimuth_m = 0  # bottom angle in minutes (24355 => facing south)

        self.manual_steps = 1

        self.tracking = False

        gpio.setmode(gpio.BCM)
        gpio.setwarnings(False)

        gpio.setup(self.pin_dir_top, gpio.OUT)
        gpio.setup(self.pin_dir_bottom, gpio.OUT)
        gpio.setup(self.pin_stp_top, gpio.OUT)
        gpio.setup(self.pin_stp_bottom, gpio.OUT)

    def turn_motor(self, pin, steps, tb):
        accelerate = [0.002, 0.0018, 0.0016, 0.0014, 0.0012, 0.001, 0.0008, 0.0006, 0.0004, 0.0002]
        if tb == 'T':
            accelerate = [0.01, 0.009, 0.008, 0.007, 0.006, 0.005, 0.004, 0.003, 0.002, 0.001]

        speed = accelerate[0]
        for i in range(steps // 2):

            if i // 20 < len(accelerate):
                speed = accelerate[i // 20]

            gpio.output(pin, True)
            sleep(speed)
            gpio.output(pin, False)
            sleep(speed)

        for i in range(steps // 2, 0, -1):

            if i < 200:
                if i // 20 <= len(accelerate):
                    speed = accelerate[i//20]

            gpio.output(pin, True)
            sleep(speed)
            gpio.output(pin, False)
            sleep(speed)

    # "21 56 30" => 1316 minut in 30 s
    # "57 23 20" => 3443 minut in 20 s

    #  5.400m = 90stopinj
    #  2.545 steps * 2 = 90stopinj
    #  2.545 steps * 2 = 5.400m
    def turn_ud(self, alt):  # alt is in minutes
        minutes = alt

        gpio.output(self.pin_dir_top, not self.altitude_m < minutes)  # turn up or down

        minutes = abs(self.altitude_m - minutes)  # calculate difference

        speed = round((minutes * 2545) / 5400)

        self.altitude_m = alt  # dms[0] * 60 + dms[1]  # set final altitude position

        self.turn_motor(self.pin_stp_top, speed * 2, 'T')  # 0.004

    #  21.600m = 360 stopinj
    #  24.355 steps * 2 = 360 stopinj
    #  24.355 steps * 2 = 21.600m
    def turn_lr(self, az):
        minutes = az

        gpio.output(self.pin_dir_bottom, self.azimuth_m < minutes)  # turn left or right

        minutes = abs(self.azimuth_m - minutes)  # calculate difference

        speed = round((minutes * 24355) / 21600)

        self.azimuth_m = az  # dms[0] * 60 + dms[1]  # set final azimuth position

        self.turn_motor(self.pin_stp_bottom, speed * 2, 'B')

    def set_location(self, p):
        # p ~ 45.801007399999996 15.1672683
        p = p.split(' ')
        lat = float(p[0])  # 45.801007399999996
        lon = float(p[1])  # 15.1672683

        lat_d = int(lat)  # lat degrees
        lon_d = int(lon)  # lon degrees

        lat_m = round((lat-lat_d) * 60)  # lat minutes
        lon_m = round((lon-lon_d) * 60)  # lon minutes

        self.dms_latitude = (lat_d, lat_m)
        self.dms_longitude = (lon_d, lon_m)

        self.initialized = True

    def locate(self, mo, dt):

        li = LocationInfo(mo.get_dec_degree(), mo.get_dec_minute(), mo.get_ra_hour(), mo.get_ra_minute(),
                          self.dms_latitude[0], self.dms_latitude[1], self.dms_longitude[0], self.dms_longitude[1],
                          dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)

        alt, az = CoordinateConversion.convert(li)

        if alt < 0:
            return 'Object is below horizon.'
        else:
            t1 = threading.Thread(target=self.turn_ud, args=[alt])
            t2 = threading.Thread(target=self.turn_lr, args=[az])
            t1.start()
            t2.start()

            t1.join()
            t2.join()

            return mo.get_object_name()

    def looking_at(self, mo, dt):

        li = LocationInfo(mo.get_dec_degree(), mo.get_dec_minute(), mo.get_ra_hour(), mo.get_ra_minute(),
                          self.dms_latitude[0], self.dms_latitude[1], self.dms_longitude[0], self.dms_longitude[1],
                          dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)

        alt, az = CoordinateConversion.convert(li)

        if alt < 0:
            return 'Object is below horizon.'
        else:
            self.altitude_m = alt
            self.azimuth_m = az
            return mo.get_object_name()

    def get_initialized(self):
        return self.initialized

    def turn_left(self):
        gpio.output(self.pin_dir_bottom, True)
        self.turn_motor(self.pin_stp_bottom, self.manual_steps * 2, 'B')

    def turn_right(self):
        gpio.output(self.pin_dir_bottom, False)
        self.turn_motor(self.pin_stp_bottom, self.manual_steps * 2, 'B')

    def turn_up(self):
        gpio.output(self.pin_dir_top, False)
        self.turn_motor(self.pin_stp_top, self.manual_steps * 2, 'T')

    def turn_down(self):
        gpio.output(self.pin_dir_top, True)
        self.turn_motor(self.pin_stp_top, self.manual_steps * 2, 'T')

    def set_manual_steps(self, steps):
        self.manual_steps = steps
