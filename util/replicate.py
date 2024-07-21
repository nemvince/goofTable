import requests
import json

def replicate(request):
    url = request['params']['request']['url']
    method = request['params']['request']['method']
    headers = request['params']['request']['headers']
    payload = request['params']['request']['postData']

    if method == 'GET':
        response = requests.get(url, headers=headers)
    else:
        response = requests.post(url, headers=headers, data=payload)

    return json.loads(response.text)

def runRequests():
    with open("req/ttv.json", 'r', encoding="utf-8") as f:
        request = json.load(f)

    # get list of timetables
    ttv = replicate(request)

    # get the latest timetable
    ttn = ttv['r']['regular']['timetables'][-1]['tt_num']

    with open("req/reg.json", "r", encoding="utf-8") as f:
        request = json.load(f)

    # replace the placeholder with the latest timetable number
    request['params']['request']['postData'] = request['params']['request']['postData'].replace("TTNUM_REPLACEME", ttn)
    
    reg = replicate(request)

    # with open("resp.json", 'w', encoding="utf-8") as f:
    #     f.write(json.dumps(reg, indent=4))
    return reg