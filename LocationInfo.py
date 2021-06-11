class LocationInfo:

    # p = 45.801007399999996 15.1672683
    def __init__(self):
        #self.lat_degrees = 0
        #self.lat_minutes = 0
        #self.lon_degrees = 0
        #self.lon_minutes = 0
        self.latitude = 0
        self.longitude = 0

    def set_location(self, p):
        p = p.split(' ')
        self.latitude = float(p[0])  # 45.801007399999996
        self.longitude = float(p[1])  # 15.1672683

        #self.lat_degrees = int(self.latitude)  # lat degrees
        #self.lon_degrees = int(self.longitude)  # lon degrees

        #self.lat_minutes = round((self.latitude - self.lat_degrees) * 60)  # lat minutes
        #self.lon_minutes = round((self.longitude - self.lon_degrees) * 60)  # lon minutes