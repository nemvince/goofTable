import json

def parseTimetable(data):
    timetable = {}
    
    # Extract relevant tables
    tables = data["r"]["dbiAccessorRes"]["tables"]
    
    # Parse classes
    classes = next((table for table in tables if table["id"] == "classes"), None)
    if classes:
        timetable["classes"] = []
        for class_ in classes["data_rows"]:
            d = {
                "id": class_['id'],
                "name": class_['name'],
                "short": class_['short']
            }
            timetable["classes"].append(d)

    # Parse groups
    groups = next((table for table in tables if table["id"] == "groups"), None)
    if groups:
        timetable["groups"] = []
        for group in groups["data_rows"]:
            d = {
                "id": group['id'],
                "divisionid": group['divisionid'],
                "name": group['name'],
                "classid": group['classid'],
                "entireclass": group['entireclass'],
            }
            timetable["groups"].append(d)

    # Parse teachers
    teachers = next((table for table in tables if table["id"] == "teachers"), None)
    if teachers:
        timetable["teachers"] = []
        for teacher in teachers["data_rows"]:
            d = {
                "id": teacher['id'],
                "name": teacher['name'],
            }
            timetable["teachers"].append(d)

    # Parse periods
    periods = next((table for table in tables if table["id"] == "periods"), None)
    if periods:
        timetable["periods"] = []
        for period in periods["data_rows"]:
          d = {
              "name": period['name'],
              "start": period['starttime'],
              "end": period['endtime']
          }
          timetable["periods"].append(d)

    # Parse classrooms
    classrooms = next((table for table in tables if table["id"] == "classrooms"), None)
    if classrooms:
        timetable["classrooms"] = []
        for classroom in classrooms["data_rows"]:
          d = {
              "id": classroom['id'],
              "name": classroom['name'],
              "short": classroom['short']
          }
          timetable["classrooms"].append(d)
    
    # Parse lessons
    lessons = next((table for table in tables if table["id"] == "lessons"), None)
    if lessons:
        timetable["lessons"] = lessons["data_rows"]
    
    return timetable

if __name__ == "__main__":
    with open("resp.json", 'r', encoding="utf-8") as f:
        data = json.load(f)

    timetable_data = parseTimetable(data)
    with open("timetable.json", 'w', encoding="utf-8") as f:
        f.write(json.dumps(timetable_data, indent=4))