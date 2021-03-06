#!/usr/bin/python

import requests

def create_session_info(session):
    return {"district_id": session["district_id"],
            "district_name": session["district_name"]}

def get_sessions(data):
        for session in data["districts"]:  
            yield create_session_info(session)

def get_districtId(stateId):
    url = "https://cdn-api.co-vin.in/api/v2/admin/location/districts/" + str(stateId)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"}
    resp = requests.get(url, params="", headers=headers, timeout=5)
    data = resp.json()
    information = [session for session in get_sessions(data)]
    resp.close()
    return information

def create_output(session_info):
    return f"{session_info['district_id']} - {session_info['district_name']}"

def getDistrictId(stateid):
    content = "\n".join([create_output(session_info) for session_info in get_districtId(stateid)])
    if not content:
        print("\n\nNo District Info available\n")
    else:
        print("\n\nChosen State, District List as below: \n\n")
        print(content)
        print("\n")
    return '\nExiting dist Id list..'

#if __name__ == "__main__":
#    print("nothing to do")