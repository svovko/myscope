from sky_object_data import messier_objects, stars


class CelestialObject:

    def __init__(self, obj_number):
        if obj_number in messier_objects:
            self.m = 'M'+str(obj_number)
            self.name = messier_objects[obj_number][0]
            self.type = messier_objects[obj_number][1]
            self.constellation = messier_objects[obj_number][2]
            self.raHour = int(messier_objects[obj_number][3])
            self.raMinute = round(float(messier_objects[obj_number][4].replace(', ', '.')))
            self.decDegree = int(messier_objects[obj_number][5] + messier_objects[obj_number][6])
            self.decMinute = int(messier_objects[obj_number][7])
            self.magnitude = messier_objects[obj_number][8]
        elif obj_number in stars:
            self.m = str(obj_number)
            self.name = stars[obj_number][0]
            self.type = 'Star'
            self.constellation = 'N/A'
            self.raHour = int(stars[obj_number][1])
            self.raMinute = int(stars[obj_number][2])
            self.decDegree = int(stars[obj_number][3] + stars[obj_number][4])
            self.decMinute = int(stars[obj_number][5])
            self.magnitude = 'N/A'

    def get_ra_hour(self):
        return self.raHour

    def get_ra_minute(self):
        return self.raMinute

    def get_dec_degree(self):
        return self.decDegree

    def get_dec_minute(self):
        return self.decMinute

    def get_object_name(self):
        return self.type + ': ' + self.name

