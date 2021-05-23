#!/usr/bin/python

import sys
import re
import time
import getpass
import cowin_stateId
import cowin_distIds
import cowin_query_distId
import cowin_query_pin
import cowin_utility

breakTime = 60  #sec
notifierType = 0 #0 - Mail, 1 - Desktop
#294 - Bengaluru, BBMP
#560048 - Bengaluru, Mahadevapura
cowin_dict = {1: {'distorpin': 'p', 'dist': '294', 'age': '45', 'dose': '1', 'pin': '560048', 'uname': 'dummy', 'pwd': 'abc', 'sname': 'xyz'}}
#, 2: {'distorpin': 'p', 'dist': '', 'age': '18', 'dose': '1', 'pin': '560048', 'uname': 'dummy', 'pwd': 'abc', 'sname': 'xyz'} }

def backToMainMenu(i, typ):
    del cowin_dict[i]
    if typ == 'int':
        print(cowin_utility.colored(0, 255, 0, "\n\nInvalid literal for int() exception caught, Pls retry ..\n\n"))
    elif typ == 'str':
        print(cowin_utility.colored(0, 255, 0, "\n\nInvalid values exception caught, Pls retry ..\n\n"))

def getUserInputs(distorpin):
    i = 0
    for q_id, q_info in cowin_dict.items():
        i = int(q_id)
        if q_info['uname'] == 'dummy' and notifierType != 1:
            break
        else:
            i = i+1
    
    #print (cowin_utility.colored(0, 255, 0, "\n\nGot i as: " + str(i)))
    if i > 1:
        cowin_dict[i] = {}
    cowin_dict[i]['distorpin'] = distorpin
    cowin_dict[i]['dist'] = ''
    cowin_dict[i]['pin'] = ''
    cowin_dict[i]['age'] = ''
    cowin_dict[i]['dose'] = ''
    cowin_dict[i]['uname'] = 'dummy'
    cowin_dict[i]['pwd'] = 'abc'
    cowin_dict[i]['sname'] = 'xyz'

    if distorpin == 'd':      
        val = input ("\nPlease enter your district id: ")
        try:
            if int(val) in range(1, 738):
                cowin_dict[i]['dist'] = val
            else:
                return 'create query by dist id failed!'
        except ValueError:
            print("\nOnly integers are allowed as input for district id")
            return backToMainMenu(i, 'int')

    elif distorpin == 'p':
        val = input ("\nPlease enter your pincode: ")
        try:
            if cowin_utility.checkPincode(val):
                cowin_dict[i]['pin'] = val
            else:
                return 'create query by pincode failed!'
        except ValueError:
            print("\nOnly integers are allowed as input for pincode")
            return backToMainMenu(i, 'int')

    val = input ("\nPlease enter your age limit: 18/45?")
    try:
        if int(val) == 18 or int(val) == 45:
            cowin_dict[i]['age'] = val
        else:
            return 'create query by dist id failed!'
    except ValueError:
        print("\nOnly integers 18/45 are allowed as input for age limit")
        return backToMainMenu(i, 'int')

    val = input ("\nPlease enter your dose number: 1/2?")
    try:
        if int(val) == 1 or int(val) == 2:
            cowin_dict[i]['dose'] = val
        else:
            return 'create query by dist id failed!'
    except ValueError:
        print("\nOnly integers 1/2 are allowed as input for dose number")
        return backToMainMenu(i, 'int')

    print (cowin_utility.colored(0, 255, 255, "\nChecking notifier type < 0-Mail, 1-Desktop > is: " + str(notifierType)))
    if notifierType != 1: #is not desktop
        if i > 1:
            val = input ("\nDo you want to resue notification <from,pwd,sendto> inputs for this query: y/n?")
            try:
                if val == 'y':
                    cowin_dict[i]['uname'] = cowin_dict[i-1]['uname']
                    cowin_dict[i]['pwd'] = cowin_dict[i-1]['pwd']
                    cowin_dict[i]['sname'] = cowin_dict[i-1]['sname']
                elif val == 'n':
                    getNoticeInputs(i)
            except ValueError:
                print("\nOnly y/n are allowed as input for notice info reuse")
                return backToMainMenu(i, 'str')
        else:
            getNoticeInputs(i)
    #print (cowin_dict)

def getNoticeInputs(i):
    val = input ("\nPlease enter your from mail id, pls make sure this account has 'Less secure app access' enabled: xxx@yyy.zzz?")
    if cowin_utility.checkMailId(val) == True:
        cowin_dict[i]['uname'] = val
    else:
        print("\nEntered invalid from email id")
        return backToMainMenu(i, 'str')
    
    val = getpass.getpass("\nPlease enter your password: ")
    cowin_dict[i]['pwd'] = val

    val = input ("\nPlease enter your send to mail id: xxx@yyy.zzz?")
    if cowin_utility.checkMailId(val) == True:
        cowin_dict[i]['sname'] = val
    else:
        print("\nEntered invalid send to email id")
        return backToMainMenu(i, 'str')

class Switcher(object):
    def indirect(self,i):
        method_name='number_'+str(i)
        method=getattr(self,method_name,lambda :'\nInvalid Entry, pls retry!')
        return method()
    #quit
    def number_q(self):
        return 'Quitting ..'
    #notifier type
    def number_0(self):
        global notifierType
        print (cowin_utility.colored(0, 255, 255, "\nCurrent notifier type < 0-Mail, 1-Desktop > is: " + str(notifierType)))
        val = input("\nPlease enter desired notifier type: ")
        try:
            if int(val) == 0 or int(val) == 1:
                #print (cowin_utility.colored(0, 255, 255, "\nChanging notifier type < 0-Mail, 1-Desktop > from: " + str(notifierType)))
                notifierType = int(val)
                print (cowin_utility.colored(0, 255, 255, "\nChanged notifier type < 0-Mail, 1-Desktop > to: " + str(notifierType)))
            else:
                raise ValueError
        except ValueError:
            print("\nOnly 0/1 are allowed as input for notifier type")
            print(cowin_utility.colored(0, 255, 0, "\n\nInvalid literal for int() exception caught, Pls retry ..\n\n"))
    #get state id list
    def number_1(self):
        return cowin_stateId.getStateId()
    #get district id list
    def number_2(self):
        my_state = input("\nPlease enter your state id: ")
        try:
            if int(my_state) in range(1, 37):
                return cowin_distIds.getDistrictId(my_state)
            else:
                return '\nget district id list failed!'
        except ValueError:
            print("\nOnly integers are allowed as input for state id")
            print(cowin_utility.colored(0, 255, 0, "\n\nInvalid literal for int() exception caught, Pls retry ..\n\n"))
    #user input for cowin query by dist id
    def number_3(self):
        print (cowin_utility.colored(0, 255, 255, "\nCreate cowin query by dist id,\n"))
        getUserInputs('d')

    #user input for cowin query by pincode
    def number_4(self):
        print (cowin_utility.colored(0, 255, 255, "\nCreate cowin query by pincode,\n"))
        getUserInputs('p')

    #current query list
    def number_5(self):
        print (cowin_utility.colored(0, 255, 255, "\nCurrent query list as below,\n"))
        #print(cowin_dict.items())
        for q_id, q_info in cowin_dict.items():
            print("\nQuery ID: ", q_id)
            for key in q_info:
                if key == 'pwd' and q_info[key] != '':
                    print(key + ': ', (q_info[key])[0:-1] + '*')
                else:
                    print(key + ': ', q_info[key])

    #delete query
    def number_6(self):
        print (cowin_utility.colored(0, 255, 255, "\nCurrent query list as below,\n"))
        #print(cowin_dict.items())
        i = 0
        for q_id, q_info in cowin_dict.items():
            print("\nQuery ID: ", q_id)
            i = i + 1
            for key in q_info:
                print(key + ': ', q_info[key])
                
        val = input("\n\nPlease select the query id to delete: ")
        try:
            if int(val) == 1 and i == 1:
                #back to default value
                cowin_dict[1]['distorpin'] = 'd'
                cowin_dict[1]['dist'] = '294'
                cowin_dict[1]['pin'] = ''
                cowin_dict[1]['age'] = '18'
                cowin_dict[1]['dose'] = '1'
                cowin_dict[1]['uname'] = 'dummy'
                cowin_dict[1]['pwd'] = ''
                cowin_dict[1]['sname'] = 'dummy'
            else:
                del cowin_dict[int(val)]
        except ValueError:
            print("\nOnly integer are allowed as input for delete query id")
            print(cowin_utility.colored(0, 255, 0, "\n\nInvalid literal for int() exception caught, Pls retry ..\n\n"))
   

    #run cowin query
    def number_7(self):
        print (cowin_utility.colored(0, 255, 255, "\nRun created cowin query,\n"))
        print (cowin_utility.colored(0, 255, 255, "\nCurrent notifier type < 0-Mail, 1-Desktop > is: " + str(notifierType)))
        
        self.number_5()

        if (input("\n\nDo you want to contune, y/n?: ") == 'y'):
            #print (cowin_dict.items())
            iteration = 0
            contLoop = True
            while contLoop != False:
                for q_id, q_info in cowin_dict.items():
                    iteration = iteration + 1
                    print("\n\nIteration >> " + str(iteration))
                    if q_info['uname'] == 'dummy' and notifierType == 0:
                        print (cowin_utility.colored(255, 0, 0, "\nInvalid notice entry, pls create query and try again..\n"))
                        contLoop = False
                        break
                    else:
                        if int(q_id) > 1:
                            executeDistPinQuery(int(q_id))
                        else:
                            executeDistPinQuery(int(q_id))
                    print (cowin_utility.colored(0, 255, 255, "\n" + str(breakTime) + " sec sleep before next query,\n"))
                    time.sleep(breakTime)
        else:
            print("\nBack to Main Menu!")

    #update sleep time
    def number_8(self):
        global breakTime
        print("\n\nCurrent buffer sleep time between query is: " + str(breakTime))
        val = input("\n\nPlease enter new sleep time in sec: ")
        try:
            if int(val) >= 30:
                breakTime = int(val)
                print("\n\nUpdated buffer sleep time between query is: " + str(breakTime))
            else:
                raise ValueError
        except ValueError:
            print("\nOnly integer are allowed as input for sleep time in seconds, min 30sec")
            print(cowin_utility.colored(0, 255, 0, "\n\nInvalid literal for int() exception caught, Pls retry ..\n\n"))

    #info on gmail less secure apps access
    def number_9(self):
        print (cowin_utility.colored(0, 0, 255, "\nGo to https://myaccount.google.com/lesssecureapps of your Google Account. You might need to sign in."))


def executeDistPinQuery(i):
    for q_id, q_info in cowin_dict.items():
        if int(q_id) == i:
            if q_info['distorpin'] == 'd':
                cowin_query_distId.cowin_distidcheck(cowin_dict[i], notifierType)
            elif q_info['distorpin'] == 'p':
                cowin_query_pin.cowin_pincodecheck(cowin_dict[i], notifierType)
            
#if __name__ == "__main__":
#    s=Switcher()
#    s.indirect(0)
#    s.indirect(5)
#    s.indirect(4)
#    s.indirect(6)
#    s.indirect(5)
#    s.indirect(7)
