#!/usr/bin/python

import requests

def create_session_info(session):
    return {"state_name": session["state_id"],
            "state_id": session["state_name"]}

def get_sessions(data):
        for session in data["states"]:  
            yield create_session_info(session)

def get_states():
    url = "https://cdn-api.co-vin.in/api/v2/admin/location/states"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"}
    resp = requests.get(url, params="", headers=headers, timeout=5)
    print("\n\nReceived response: " + str(resp))
    data = resp.json()
    information = [session for session in get_sessions(data)]
    resp.close()
    return information

def create_output(session_info):
    return f"{session_info['state_name']} - {session_info['state_id']}"

def getStateId():
    content = "\n".join([create_output(session_info) for session_info in get_states()])
    if not content:
        print("\n\nNo State Info available!\n")
    else:
        print("\n\nState List as below: \n\n")
        print(content)
        print("\n")
    return '\nExiting State Id list ..'

#if __name__ == "__main__":
#    print("nothing to do")
