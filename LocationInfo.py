class LocationInfo:

    def __init__(self, dd, dm, rh, rm, lad, lam, lod, lom, y, m, d, hour, minute, second):
        self.dec_degrees = dd
        self.dec_minutes = dm

        self.ra_hours = rh
        self.ra_minutes = rm

        self.lat_degrees = lad
        self.lat_minutes = lam
        self.lon_degrees = lod
        self.lon_minutes = lom

        self.dtg_year = y
        self.dtg_month = m
        self.dtg_day = d
        self.dtg_hour = hour
        self.dtg_minute = minute
        self.dtg_second = second

    def printLI(self):
        print('RA:', self.ra_hours, self.ra_minutes)
        print('DEC:', self.dec_degrees, self.dec_minutes)
        print('LATITUDE:', self.lat_degrees, self.lat_minutes)
        print('LONGITUDE:', self.lon_degrees, self.lon_minutes)
        print('DATE:', self.dtg_year, self.dtg_month, self.dtg_day)
        print('TIME:', self.dtg_hour, self.dtg_minute, self.dtg_second)
