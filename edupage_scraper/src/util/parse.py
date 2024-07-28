from util.data.structures import (
    Class,
    Classroom,
    Group,
    Lesson,
    Period,
    Teacher,
    Timetable,
)


def parseTimetable(data):
    timetable = {}

    # extract relevant tables
    tables = data["r"]["dbiAccessorRes"]["tables"]

    for table in tables:
        timetable[table["id"]] = table["data_rows"]

    # dump data into structured classes
    timetable_data = Timetable()
    for x in timetable["classes"]:
        timetable_data.classes.append(Class(x))

    for x in timetable["groups"]:
        timetable_data.groups.append(Group(x))

    for x in timetable["teachers"]:
        timetable_data.teachers.append(Teacher(x))

    for x in timetable["periods"]:
        timetable_data.periods.append(Period(x))

    for x in timetable["classrooms"]:
        timetable_data.classrooms.append(Classroom(x))

    for x in timetable["lessons"]:
        timetable_data.lessons.append(Lesson(x))

    return timetable_data
