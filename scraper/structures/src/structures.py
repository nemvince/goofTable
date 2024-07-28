import datetime
import uuid


class Class:
    def __init__(self, class_):
        self.id = uuid.uuid4()
        self.edu_id = class_["id"]
        self.name = class_["name"]
        self.short = class_["short"]


class Group:
    def __init__(self, group):
        self.id = uuid.uuid4()
        self.edu_id = group["id"]
        self.divisionid = group["divisionid"]
        self.name = group["name"]
        self.classid = group["classid"]
        self.entireclass = group["entireclass"]


class Teacher:
    def __init__(self, teacher):
        self.id = uuid.uuid4()
        self.edu_id = teacher["id"]
        self.name = teacher["name"]


class Period:
    def __init__(self, period):
        self.id = uuid.uuid4()
        self.name = period["name"]
        self.start = datetime.datetime.strptime(period["starttime"], "%H:%M").time()
        self.end = datetime.datetime.strptime(period["endtime"], "%H:%M").time()


class Classroom:
    def __init__(self, classroom):
        self.id = uuid.uuid4()
        self.edu_id = classroom["id"]
        self.name = classroom["name"]
        self.short = classroom["short"]


class Division:
    def __init__(self, division):
        self.id = uuid.uuid4()
        self.edu_id = division["id"]
        self.groupids = division["groupids"]


class Lesson:
    def __init__(self, lesson):
        self.id = uuid.uuid4()
        self.edu_id = lesson["id"]
        self.groupids = lesson["groupids"]
        self.subjectid = lesson["subjectid"]
        self.teacherids = lesson["teacherids"]
        self.periodid = lesson["count"]
        self.duration = lesson["durationperiods"]


class Timetable:
    def __init__(self):
        self.classes: list[Class] = []
        self.groups: list[Group] = []
        self.teachers: list[Teacher] = []
        self.periods: list[Period] = []
        self.classrooms: list[Classroom] = []
        self.divisions: list[Division] = []
        self.lessons: list[Lesson] = []
