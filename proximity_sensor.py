class proximity_sensor(object):
    
    def __init__(self, teachers, students, distance_threshold):
        self.teachers = teachers
        self.students = students
        self.distance_threshold = distance_threshold
    
    #returns a map of tags like:
        #{type of tag
    def tags_nearby(self):
        return none