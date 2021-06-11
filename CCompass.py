import smbus
import time
import math

class Compass:
    
    def __init__(self):

        self.bus = smbus.SMBus(1)

        ''' Set acceleration data registers '''
        self.bus.write_byte_data(0x19, 0x20, 0x27)
        self.bus.write_byte_data(0x19, 0x23, 0x00)

        ''' Set magnetic data registers '''
        self.bus.write_byte_data(0x1E, 0x02, 0x00)
        self.bus.write_byte_data(0x1E, 0x00, 0x10)
        self.bus.write_byte_data(0x1E, 0x01, 0x20)

        self.acceleration = (0,0,0)
        self.magnetic = (0,0,0)

    def updateAcceleration(self):

        # Read accl X-axis data
        data0x = self.bus.read_byte_data(0x19, 0x28)
        data1x = self.bus.read_byte_data(0x19, 0x29)

        # Read Accl Y-axis data
        data0y = self.bus.read_byte_data(0x19, 0x2A)
        data1y = self.bus.read_byte_data(0x19, 0x2B)

        # Read Accl Z-axis data
        data0z = self.bus.read_byte_data(0x19, 0x2C)
        data1z = self.bus.read_byte_data(0x19, 0x2D)

        # save acceleration data
        self.acceleration = (convert_data(data0x, data1x), convert_data(data0y, data1y), convert_data(data0z, data1z))


    def updateMagnetic(self):

        # Read magnetic X-axis data
        data0x = self.bus.read_byte_data(0x1E, 0x03)
        data1x = self.bus.read_byte_data(0x1E, 0x04)

        # Read magnetic Y-axis data
        data0y = self.bus.read_byte_data(0x1E, 0x07)
        data1y = self.bus.read_byte_data(0x1E, 0x08)

        # Read magnetic Z-axis data
        data0z = self.bus.read_byte_data(0x1E, 0x05)
        data1z = self.bus.read_byte_data(0x1E, 0x06)


        # save magnetic data
        self.magnetic = (convert_data(data0x, data1x), convert_data(data0y, data1y), convert_data(data0z, data1z))

    def getHeading(self):
        self.updateMagnetic()
        heading = math.degrees(math.atan2(self.magnetic[1], self.magnetic[0]))
        print ("Heading: ", round(heading, 2))
        return heading

def convert_data(self, data0, data1):
    x = (data0 << 8) | data1 # or data0 * 256 + data1
    if x > 32767:
        x -= 65536
    return x
