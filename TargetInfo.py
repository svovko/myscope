#from sky_object_data import get_object_by_id
import sky_object_data


class TargetInfo:

    def __init__(self):
        self.obj_id = 0

        self.ra_hours = 0
        self.ra_minutes = 0
        self.ra_seconds = 0

        self.dec_degrees = 0
        self.dec_minutes = 0
        self.dec_seconds = 0

        self.type = 'N/A'
        self.constellation = 'N/A'
        self.messier_refference = 'N/A'
        self.magnitude = 'N/A'
        self.note = 'N/A'

    def set_target(self, obj_id):
        self.obj_id = obj_id
        obj = sky_object_data.get_object_by_id(self.obj_id)  # '85' : ['*', '21:42:05.66', '+51:11:22.6', 'Cyg', '', '4.69', 'Azelfafage'],

        ra = obj[1].split(':') # e. g.: '21:42:05.66' 
        self.ra_hours = int(ra[0])
        self.ra_minutes = int(ra[1])
        self.ra_seconds = float(ra[2])

        dec = obj[2].split(':') # e. g.: '+51:11:22.6'
        self.dec_degrees = int(dec[0])
        self.dec_minutes = int(dec[1])
        self.dec_seconds = float(dec[2])

        self.type = obj[0] # e. g.: '*'
        self.constellation = obj[3]
        self.messier_refference = obj[4]
        self.magnitude = obj[5]
        self.note = obj[6] + ' (RA: ' + obj[1] + ', DEC: ' + obj[2] + ')'

    def izpis(self):
        print("Note: {}, Ra: {}, Dec: {}".format(self.note, str(self.ra_hours)+':'+str(self.ra_minutes), str(self.dec_degrees)+':'+str(self.dec_minutes)))

    def get_obj(self):
        return f'{self.obj_id} - {self.note}'
