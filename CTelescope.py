import RPi.GPIO as gpio
from time import sleep
from LocationInfo import LocationInfo
import threading
import helper_functions


# SMALL GEAR TEETH COUNT = 24  # number of teeth
# BIG GEAR TEETH COUNT = 162  # number of teeth
# RATIO = 6.75
# STEPS PER REVOLUTION = 3200  # with microstepping
# 1 STEP = 1 ARC MINUTE

# for 1 arc second step I need gear reduction ratio of 405:1
# self.bottom_steps_per_second = 1 # 1 step = 1 arc second (given the ratio 405)
# self.top_steps_per_second = 1 # 1 step = 1 arc second


class Telescope:

    def __init__(self, pd_t, pd_b, ps_t, ps_b):
        self.pin_dir_top = pd_t
        self.pin_dir_bottom = pd_b

        self.pin_stp_top = ps_t
        self.pin_stp_bottom = ps_b

        self.altitude_m = 0  # top angle in minutes
        self.azimuth_m = 0  # bottom angle in minutes
        
        # 1 step = 1 minute
        self.manual_steps = 1

        # 1 step = 1 arc minute
        self.bottom_steps_per_minute = 1
        self.top_steps_per_minute = 1

        self.min_speed = 0.01
        self.max_speed = 0.001

        self.tracking = False

        gpio.setmode(gpio.BCM)
        gpio.setwarnings(False)

        gpio.setup(self.pin_dir_top, gpio.OUT)
        gpio.setup(self.pin_dir_bottom, gpio.OUT)
        gpio.setup(self.pin_stp_top, gpio.OUT)
        gpio.setup(self.pin_stp_bottom, gpio.OUT)

    def make_step(self, pin, delay):
        gpio.output(pin, True)
        sleep(delay)
        gpio.output(pin, False)
        sleep(delay)

    def turn_motor(self, pin, steps):

        # 3200 steps = ful revolution
        if steps < 400:
            acc_percent = .4
        elif steps < 800:
            acc_percent = .3
        elif steps < 1600:
            acc_percent = .2
        elif steps < 3200:
            acc_percent = .1
        else:
            acc_percent = .05

        acc_steps = dec_steps = int(steps * acc_percent)

        delay = self.min_speed

        for i in range(acc_steps):
            delay = round(helper_functions.valmap(i + 1, 1, acc_steps, self.min_speed, self.max_speed), 5)
            self.make_step(pin, delay)

        for i in range(1, steps - acc_steps - dec_steps + 1):
            self.make_step(pin, delay)

        for i in range(dec_steps):
            delay = round(helper_functions.valmap(i + 1, dec_steps, 1, self.min_speed, self.max_speed), 5)
            self.make_step(pin, delay)


    # ****************** bottom motor ***********************
    def turn_left(self, delta_minutes):  # az is in minutes (convert function returns az converted to minutes)
        print('Turning left for', delta_minutes, 'minutes.')
        gpio.output(self.pin_dir_bottom, False)  # turn left or right
        if delta_minutes > 0:
            self.turn_motor(self.pin_stp_bottom, delta_minutes)

    def turn_right(self, delta_minutes):  # az is in minutes (convert function returns az converted to minutes)
        print('Turning right for', delta_minutes, 'minutes.')
        gpio.output(self.pin_dir_bottom, True)  # turn left or right
        if delta_minutes > 0:
            self.turn_motor(self.pin_stp_bottom, delta_minutes)

    # ****************** top motor ***********************
    def turn_up(self, delta_minutes):  # az is in minutes (convert function returns az converted to minutes)
        print('Turning up for', delta_minutes, 'minutes.')
        gpio.output(self.pin_dir_top, False)  # turn up or down
        if delta_minutes > 0:
            self.turn_motor(self.pin_stp_top, delta_minutes)

    def turn_down(self, delta_minutes):  # az is in minutes (convert function returns az converted to minutes)
        print('Turning down for', delta_minutes, 'minutes.')
        gpio.output(self.pin_dir_top, True)  # turn up or down
        if delta_minutes > 0:
            self.turn_motor(self.pin_stp_top, delta_minutes)

    def locate(self, ti, li):  # target info & location info

        alt, az = helper_functions.convert(ti, li)  # gets altitude and azimuth in decimal degrees
        print('altitude (deg):', alt)
        print('azimuth (deg:)', az)

        alt = helper_functions.real2minutes(alt) # converts decimal degrees to minutes
        az = helper_functions.real2minutes(az) # converts decimal degrees to minutes
        print('altitude (min): ', alt)
        print('azimuth (min):', az)

        if alt < 0:
            return 'Object is below horizon.'
        else:
            t1 = t2 = None
            if alt > self.altitude_m: # turn up
                t1 = threading.Thread(target=self.turn_up, args=[abs(alt-self.altitude_m)])
                t1.start()
                self.altitude_m = alt
            elif alt < self.altitude_m: # turn down
                t1 = threading.Thread(target=self.turn_down, args=[abs(alt-self.altitude_m)])
                t1.start()
                self.altitude_m = alt

            if az > self.azimuth_m: # turn right
                t2 = threading.Thread(target=self.turn_right, args=[abs(az-self.azimuth_m)])
                t2.start()
                self.azimuth_m = az
            elif az < self.azimuth_m: # turn left
                t2 = threading.Thread(target=self.turn_left, args=[abs(az-self.azimuth_m)])
                t2.start()
                self.azimuth_m = az

            if t1:
                t1.join()
            if t2:
                t2.join()

            return f'NOTE: {ti.note} | OBJID: {ti.obj_id} | POS:({self.return_position()})'

    def stop_tracking(self):
        self.tracking = False

    def start_tracking(self, ti, li):
        self.tracking = True
        while self.tracking:
            self.locate(ti, li)
            sleep(1)

    def looking_at(self, ti, li):

        alt, az = helper_functions.convert(ti, li)

        if alt < 0:
            return 'Object is below horizon.'
        else:
            self.altitude_m = helper_functions.real2minutes(alt)
            self.azimuth_m = helper_functions.real2minutes(az)
            return f'NOTE: {ti.note} | OBJID: {ti.obj_id} | POS:({self.return_position()})'

    def reset_position(self):
        self.altitude_m = 0
        self.azimuth_m = 0

    def set_manual_steps(self, steps):
        self.manual_steps = steps

    def return_position(self):
        return  f'ALT: {helper_functions.min2DM(self.altitude_m)}, AZ: {helper_functions.min2DM(self.azimuth_m)}'


    def turn_to_altitude(self, alt_minutes):
        if alt_minutes > self.altitude_m: # turn up
            self.turn_up(abs(alt_minutes-self.altitude_m))
            self.altitude_m = alt_minutes
        elif alt_minutes < self.altitude_m: # turn down
            self.turn_down(abs(alt_minutes-self.altitude_m))
            self.altitude_m = alt_minutes

        return f'POS:({self.return_position()})'

    def turn_to_azimuth(self, az_minutes):
        if az_minutes > self.azimuth_m: # turn right
            self.turn_right(abs(az_minutes-self.azimuth_m))
            self.azimuth_m = az_minutes
        elif az_minutes < self.azimuth_m: # turn left
            self.turn_left(abs(az_minutes-self.azimuth_m))
            self.azimuth_m = az_minutes

        return f'POS:({self.return_position()})'