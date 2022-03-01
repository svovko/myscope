import math
import datetime


# compute horizon coordinates
# from ra, dec, lat, lon, and utc
# ra, dec, lat, lon in degrees
# utc is a Date object
# results returned in hrz_altitude, hrz_azimuth
def convert(ti, li):

    ra = ra2real(ti.ra_hours, ti.ra_minutes, ti.ra_seconds)
    dec = dms2real(ti.dec_degrees, ti.dec_minutes, ti.dec_seconds)

    # compute hour angle in degrees
    ha = mean_sidereal_time(li.longitude) - ra
    if ha < 0:
        ha = ha + 360

    # convert degrees to radians
    ha = math.radians(ha)
    dec = math.radians(dec)

    lat = math.radians(li.latitude)

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

    return hrz_altitude, hrz_azimuth


# Compute the Mean Sidereal Time in units of degrees.
# Use lon := 0 to get the Greenwich MST.
# East longitudes are positive; West longitudes are negative
# returns: time in degrees
def mean_sidereal_time(lon):

    dt = datetime.datetime.now()

    year = dt.year
    month = dt.month
    day = dt.day
    hour = dt.hour - 1  # -1 zaradi +1 timezone (UTC)
    minute = dt.minute
    second = dt.second

    if month == 1 or month == 2:
        year = year - 1
        month = month + 12

    a = year // 100
    b = 2 - a + a // 4
    c = math.floor(365.25 * year)
    d = math.floor(30.6001 * (month + 1))

    # days since J2000.0
    jd = b + c + d - 730550.5 + day + (hour + minute / 60 + second / 3600) / 24

    # julian centuries since J2000.0
    jt = jd / 36525

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
def ra2real(hr, minutes, sec):
    return 15 * (hr + (minutes / 60) + (sec / 3600))


# convert angle(deg, min) to degrees as real
def dms2real(deg, minutes, sec):
    if deg < 0:
        return deg - (minutes / 60) - (sec / 3600)
    else:
        return deg + (minutes / 60) + (sec / 3600)


def real2minutes(real_degrees):
    deg = real_degrees // 1
    minutes = (real_degrees - deg) * 60
    return round(deg * 60 + minutes)

def real2seconds(real_degrees):
    return round(real_degrees * 3600)


def is_visible(ti, li):
    alt, az = convert(ti, li)
    return alt > 0


def min2DM(min):
    degree_sign= u'\N{DEGREE SIGN}'
    return f'{min//60}{degree_sign} {min%60}"'

def seconds2DMS(sec):
    degree_sign= u'\N{DEGREE SIGN}'
    return f'{sec//3600}{degree_sign} {(sec%3600)//60}" {((sec%3600)%60)/60}\''

def deg2HMS(ra='', dec=''):
    #['*', '2:31:49', '89:15:50', 'UMi', '', '2.13', 'Polaris'],
    RA, DEC, rs, ds = '', '', '', ''
    if dec:
        if str(dec)[0] == '-':
            ds, dec = '-', abs(dec)
        else:
            ds = '+'

        deg = int(dec)
        decM = abs(int((dec - deg) * 60))

        #if round:
        #    decS = int((abs((dec - deg) * 60) - decM) * 60)
        #else:
        #    decS = (abs((dec - deg) * 60) - decM) * 60
        decS = round((abs((dec - deg) * 60) - decM) * 60, 2)

        DEC = '{0}{1:02d}:{2:02d}:{3:04.1f}'.format(ds, deg, decM, decS)

    if ra:
        if str(ra)[0] == '-':
            rs, ra = '-', abs(ra)

        raH = int(ra / 15)
        raM = int(((ra / 15) - raH) * 60)

        #if round:
        #    raS = int(((((ra / 15) - raH) * 60) - raM) * 60)
        #else:
        #    raS = ((((ra / 15) - raH) * 60) - raM) * 60
        raS = round(((((ra / 15) - raH) * 60) - raM) * 60, 2)

        RA = '{0}{1:02d}:{2:02d}:{3:05.2f}'.format(rs, raH, raM, raS)

    if ra and dec:
        return (RA, DEC)
    else:
        return RA or DEC


def valmap(x, in_min, in_max, out_min, out_max):
    if in_min == in_max:
        return out_min
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
