import math


def convert(li):
    ra = ra2real(li.ra_hours, li.ra_minutes)
    dec = dms2real(li.dec_degrees, li.dec_minutes)
    lat = dms2real(li.lat_degrees, li.lat_minutes)
    lon = dms2real(li.lon_degrees, li.lon_minutes)

    return coord_to_horizon(li.dtg_year, li.dtg_month, li.dtg_day,  # date
                            li.dtg_hour, li.dtg_minute, li.dtg_second,  # time
                            ra, dec,  # DSO coordinates
                            lat, lon)  # observer location



# compute horizon coordinates
# from ra, dec, lat, lon, and utc
# ra, dec, lat, lon in degrees
# utc is a Date object
# results returned in hrz_altitude, hrz_azimuth
def coord_to_horizon(dtg_year, dtg_month, dtg_day, dtg_hour, dtg_minute, dtg_second, ra, dec, lat, lon):
    # compute hour angle in degrees
    ha = mean_sidereal_time(dtg_year, dtg_month, dtg_day, dtg_hour, dtg_minute, dtg_second, lon) - ra
    if ha < 0:
        ha = ha + 360

    # convert degrees to radians
    ha = math.radians(ha)
    dec = math.radians(dec)
    lat = math.radians(lat)

    # compute altitude in radians
    alt = math.asin(math.sin(dec) * math.sin(lat) + math.cos(dec) * math.cos(lat) * math.cos(ha))

    # compute azimuth in radians
    # divide by zero error at poles or if alt = 90 deg
    az = math.acos((math.sin(dec) - math.sin(alt) * math.sin(lat)) / (math.cos(alt) * math.cos(lat)))

    # convert radians to degrees
    hrz_altitude = math.degrees(alt)
    hrz_azimuth = math.degrees(az)

    # choose hemisphere
    if math.sin(ha) > 0:
        hrz_azimuth = 360 - hrz_azimuth

    return real2minutes(hrz_altitude), real2minutes(hrz_azimuth)


# Compute the Mean Sidereal Time in units of degrees.
# Use lon := 0 to get the Greenwich MST.
# East longitudes are positive; West longitudes are negative
# returns: time in degrees
def mean_sidereal_time(year, month, day, hour, minute, second, lon):
    hour -= 1  # -1 zaradi +1 timezone (UTC)

    if month == 1 or month == 2:
        year = year - 1
        month = month + 12

    a = year // 100
    b = 2 - a + a // 4
    c = math.floor(365.25 * year)
    d = math.floor(30.6001 * (month + 1))

    # days since J2000.0
    jd = b + c + d - 730550.5 + day + (hour + minute / 60.0 + second / 3600.0) / 24.0

    # julian centuries since J2000.0
    jt = jd / 36525.0

    # the mean sidereal time in degrees
    mst = 280.46061837 + 360.98564736629 * jd + 0.000387933 * jt * jt - jt * jt * jt / 38710000 + lon

    # in degrees modulo 360.0
    if mst > 0.0:
        while mst > 360.0:
            mst = mst - 360.0
    else:
        while mst < 0.0:
            mst = mst + 360.0

    return mst


# convert right ascension(hours, minutes) to degrees as real
def ra2real(hr, minutes):
    return 15 * (hr + minutes / 60)


# convert angle(deg, min) to degrees as real
def dms2real(deg, minutes):
    if deg < 0:
        return deg - minutes / 60

    return deg + minutes / 60


def real2minutes(real_degrees):
    deg = real_degrees // 1
    minutes = (real_degrees - deg) * 60
    return round(deg * 60 + minutes)
