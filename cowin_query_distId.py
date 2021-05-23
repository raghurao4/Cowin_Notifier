#!/usr/bin/python

from datetime import datetime

import sys, getopt
import os
import requests
import cowin_utility

def create_session_info(center, session):
    return {"name": center["name"],
            "date": session["date"],
            "capacity": session["available_capacity"],
            "capacity1": session["available_capacity_dose1"],
            "capacity2": session["available_capacity_dose2"],
            "age_limit": session["min_age_limit"]}

def get_sessions(data):
    for center in data["centers"]:
        for session in center["sessions"]:
            yield create_session_info(center, session)

def get_for_seven_days(start_date, iDistId, iageLimit, iDose):
    url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
    params = {"district_id": iDistId, "date": start_date.strftime("%d-%m-%Y")}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"}
    resp = requests.get(url, params=params, headers=headers, timeout=5)
    data = resp.json()
    if int(iDose) == 1:
        information = [session for session in get_sessions(data) if ((session["age_limit"] == int(iageLimit)) and (session["capacity1"] > 0) )]
    elif int(iDose) == 2:
        information = [session for session in get_sessions(data) if ((session["age_limit"] == int(iageLimit)) and (session["capacity2"] > 0) )]
    else:
        print("\n\nDist query - Unusual Dose#. I am here .......")
        information = [session for session in get_sessions(data)]
    resp.close()
    return information

def create_output(session_info):
    return f"{session_info['date']} - {session_info['name']} - {session_info['age_limit']} - {session_info['capacity']} - {session_info['capacity1']} - {session_info['capacity2']}"

#"Date - Center - AgeLimit - TotalCapacity - 1stDoseCapacity - 2ndDoseCapacity"
def cowin_distidcheck(check):
    #print(check.items())
    for q_id, q_info in check.items():
        #if int(q_id) == iter:
        iDistId = check['dist']   
        iageLimit = check['age']
        iDose = check['dose']
        username = check['uname']
        password = check['pwd']
        sendtoname = check['sname']
    
    #password hidden
    print("\n\nGot District check values .. " + iDistId + ", " + iageLimit + ", " +  iDose  + ", " + username + ", " +  "*pwd_not_print*" + ", " + sendtoname + "\n\n" )

    print(get_for_seven_days(datetime.today(), iDistId, iageLimit, iDose))
    content = "\n".join([create_output(session_info) for session_info in get_for_seven_days(datetime.today(), iDistId, iageLimit, iDose)])
    
    if not content:
        print("\nDistId " + iDistId + "# No availability found!")
    else:
        sub = "Vaccination Slot By DistId Open"
        cowin_utility.sendMail(username, password, sendtoname, sub, content)

#if __name__ == "__main__":
#    print("nothing to do")
    