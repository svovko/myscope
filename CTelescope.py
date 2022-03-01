import RPi.GPIO as gpio
from time import sleep
from LocationInfo import LocationInfo
import threading
import helper_functions

# for 1 arc second step I need gear reduction ratio of 405:1
# self.bottom_steps_per_second = 1 # 1 step = 1 arc second (given the ratio 405)
# self.top_steps_per_second = 1 # 1 step = 1 arc second
# In sixtinth step: 3200 steps / 360 degrees
# Gear reduction: 9 x 9 x 5 = 405
# Steps per full revolution: 1.296.000 (3200 * 405)
# Steps per degree: 3600 (1.296.000 / 360)
# Steps per arc minute: 60 (3600 / 60)
# Steps per arc second: 1 (60 / 60)


class Telescope:

    def __init__(self, pd_t, pd_b, ps_t, ps_b): # 5, 13, 6, 19

        # set direction pins
        self.pin_dir_top = pd_t
        self.pin_dir_bottom = pd_b

        # set step pins
        self.pin_stp_top = ps_t
        self.pin_stp_bottom = ps_b

        # Telescope start position
        self.altitude_seconds = 324000 # (90 * 3600) top angle in minutes (pointing straight up)
        self.azimuth_seconds = 0  # bottom angle in minutes (0 = pointing north)

        # 1 step = 1 arc second
        self.bottom_steps_per_second = 1 
        self.top_steps_per_second = 1

        # bottom and top motor speed
        self.speed_bottom = 0.00005
        self.speed_top = 0.00005

        # turning status
        self.tracking = False
        self.turning_top = False
        self.turning_bottom = False

        # GPIO settings
        gpio.setmode(gpio.BCM)
        gpio.setwarnings(False)

        # PIN settings
        gpio.setup(self.pin_dir_top, gpio.OUT)
        gpio.setup(self.pin_dir_bottom, gpio.OUT)
        gpio.setup(self.pin_stp_top, gpio.OUT)
        gpio.setup(self.pin_stp_bottom, gpio.OUT)

    def reset_position(self):
        self.altitude_seconds = 324000
        self.azimuth_seconds = 0


    # + Actual turning of the motors +
    # NOTE: direction must be set before calling this method
    def make_step_left(self):
        gpio.output(self.pin_stp_bottom, True)
        sleep(self.speed_bottom)
        gpio.output(self.pin_stp_bottom, False)
        sleep(self.speed_bottom)
        self.azimuth_seconds -= 1

    # NOTE: direction must be set before calling this method
    def make_step_right(self):
        gpio.output(self.pin_stp_bottom, True)
        sleep(self.speed_bottom)
        gpio.output(self.pin_stp_bottom, False)
        sleep(self.speed_bottom)
        self.azimuth_seconds += 1

    # NOTE: direction must be set before calling this method
    def make_step_down(self):
        gpio.output(self.pin_stp_top, True)
        sleep(self.speed_top)
        gpio.output(self.pin_stp_top, False)
        sleep(self.speed_top)
        self.altitude_seconds -= 1

    # NOTE: direction must be set before calling this method
    def make_step_up(self):
        gpio.output(self.pin_stp_top, True)
        sleep(self.speed_top)
        gpio.output(self.pin_stp_top, False)
        sleep(self.speed_top)
        self.altitude_seconds += 1
    # - Actual turning of the motors -




    # + These methods are called when locating objects +
    # ****************** bottom motor ***********************
    def turn_left(self, seconds):  
        # print('Turning left for', delta_minutes, 'minutes.')
        gpio.output(self.pin_dir_bottom, True)  # turn left or right
        for i in range(seconds):
            self.make_step_left()

    def turn_right(self, seconds):  
        # print('Turning right for', delta_minutes, 'minutes.')
        gpio.output(self.pin_dir_bottom, False)  # turn left or right
        for i in range(seconds):
            self.make_step_right()

    # ****************** top motor ***********************
    def turn_up(self, seconds):  
        # print('Turning up for', delta_minutes, 'minutes.')
        gpio.output(self.pin_dir_top, False)  # turn up or down
        for i in range(seconds):
            self.make_step_up()

    def turn_down(self, seconds):  
        # print('Turning down for', delta_minutes, 'minutes.')
        gpio.output(self.pin_dir_top, True)  # turn up or down
        for i in range(seconds):
            self.make_step_down()
    # - These methods are called when locating objects -




    # + These methods are called when we manually hold and press to rotate motors +
    def start_bottom_motor_left(self):
        gpio.output(self.pin_dir_bottom, True) 
        self.turning_bottom = True
        while self.turning_bottom:
            self.make_step_left()

    def start_bottom_motor_right(self):
        gpio.output(self.pin_dir_bottom, False) 
        self.turning_bottom = True
        while self.turning_bottom:
            self.make_step_right()

    def start_top_motor_up(self):
        gpio.output(self.pin_dir_top, False) 
        self.turning_top = True
        while self.turning_top:
            self.make_step_up()

    def start_top_motor_down(self):
        gpio.output(self.pin_dir_top, True) 
        self.turning_top = True
        while self.turning_top:
            self.make_step_down()
    # - These methods are called when we manually hold and press to rotate motors -




    def start_turning_left(self):
        t = threading.Thread(target=self.start_bottom_motor_left)
        t.start()
        t.join()
        return self.return_position()

    def start_turning_right(self):
        t = threading.Thread(target=self.start_bottom_motor_right)
        t.start()
        t.join()
        return self.return_position()

    def start_turning_up(self):
        t = threading.Thread(target=self.start_top_motor_up)
        t.start()
        t.join()
        return self.return_position()

    def start_turning_down(self):
        t = threading.Thread(target=self.start_top_motor_down)
        t.start()
        t.join()
        return self.return_position()


    

    def stop_turning_left(self):
        self.turning_bottom = False

    def stop_turning_right(self):
        self.turning_bottom = False

    def stop_turning_up(self):
        self.turning_top = False

    def stop_turning_down(self):
        self.turning_top = False

    def locate(self, ti, li):  # target info & location info

        alt, az = helper_functions.convert(ti, li)  # gets altitude and azimuth in decimal degrees
        print('altitude (deg):', alt)
        print('azimuth (deg:)', az)

        alt = helper_functions.real2seconds(alt) # converts decimal degrees to minutes
        az = helper_functions.real2seconds(az) # converts decimal degrees to minutes
        print('altitude (in seconds): ', alt)
        print('azimuth (in seconds):', az)

        if alt < 0:
            return 'Object is below horizon.'
        else:
            t1 = t2 = None
            if alt > self.altitude_seconds: # turn up
                t1 = threading.Thread(target=self.turn_up, args=[abs(alt-self.altitude_seconds)])
                t1.start()
            elif alt < self.altitude_seconds: # turn down
                t1 = threading.Thread(target=self.turn_down, args=[abs(alt-self.altitude_seconds)])
                t1.start()

            if az > self.azimuth_seconds: # turn right
                t2 = threading.Thread(target=self.turn_right, args=[abs(az-self.azimuth_seconds)])
                t2.start()
            elif az < self.azimuth_seconds: # turn left
                t2 = threading.Thread(target=self.turn_left, args=[abs(az-self.azimuth_seconds)])
                t2.start()

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

    # Set scope initial position (when pointing a scope to a known celestial object)
    def looking_at(self, ti, li):

        alt, az = helper_functions.convert(ti, li)

        if alt < 0:
            return 'Object is below horizon.'
        else:
            self.altitude_seconds = helper_functions.real2seconds(alt)
            self.azimuth_seconds = helper_functions.real2seconds(az)
            return f'NOTE: {ti.note} | OBJID: {ti.obj_id} | POS:({self.return_position()})'

    # def set_manual_steps(self, steps):
    #     self.manual_steps = steps

    # returns current scope position for altitude and azimuth respectively in string format D° M" s'
    def return_position(self):
        return  f'ALT: {helper_functions.seconds2DMS(self.altitude_seconds)}, AZ: {helper_functions.seconds2DMS(self.azimuth_seconds)}'

    def turn_to_altitude(self, alt_seconds):
        if alt_seconds > self.altitude_seconds: # turn up
            self.turn_up(abs(alt_seconds-self.altitude_seconds))
        elif alt_seconds < self.altitude_seconds: # turn down
            self.turn_down(abs(alt_seconds-self.altitude_seconds))

        # returns new position
        return f'POS:({self.return_position()})'

    def turn_to_azimuth(self, az_seconds):
        if az_seconds > self.azimuth_seconds: # turn right
            self.turn_right(abs(az_seconds-self.azimuth_seconds))
        elif az_seconds < self.azimuth_seconds: # turn left
            self.turn_left(abs(az_seconds-self.azimuth_seconds))

        # returns new position
        return f'POS:({self.return_position()})'

    def set_top_speed(self, speed):
        self.speed_top = speed

    def set_bottom_speed(self, speed):
        self.speed_bottom = speed
