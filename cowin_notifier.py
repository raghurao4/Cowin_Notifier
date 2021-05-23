#!/usr/bin/python

import sys
import cowin_switcher
import cowin_utility

def main():
    text = '\n######################################################################'
    text = text + '\n#    Hello, Welcome to CoWin query notification autobot by distId!   #'
    text = text + '\n######################################################################\n\n'
    colored_text = cowin_utility.colored(0, 255, 255, text)
    print(colored_text)
    
    s=cowin_switcher.Switcher()
    choice = ''

    while choice != 'q':
        print(cowin_utility.colored(0, 0, 255, "\n[0] Enter 0 to set preference to Mail or Desktop notification."))
        print(cowin_utility.colored(0, 0, 255, "[1] Enter 1 to get state id list."))
        print(cowin_utility.colored(0, 0, 255, "[2] Enter 2 to get district id list."))
        print(cowin_utility.colored(0, 0, 255, "[3] Enter 3 to create cowin query by dist id."))
        print(cowin_utility.colored(0, 0, 255, "[4] Enter 4 to create cowin query by pincode."))
        print(cowin_utility.colored(0, 0, 255, "[5] Enter 5 to print current query."))
        print(cowin_utility.colored(0, 0, 255, "[6] Enter 6 to delete current query."))
        print(cowin_utility.colored(0, 0, 255, "[7] Enter 7 to run created queries until interrupted."))
        print(cowin_utility.colored(0, 0, 255, "[8] Enter 8 to update buffer sleep time between query, default is 60sec, min 30sec."))
        print(cowin_utility.colored(0, 0, 255, "[9] Enter 9 help with less secure apps access on google account."))
        print(cowin_utility.colored(255, 0, 0, "[q] Enter q to quit gracefully ^.^"))
        print(cowin_utility.colored(255, 0, 0, "[Ctrl+c] Press Ctrl+c to Exit the application."))

        try:
            choice = input("\nWhat would you like to do? ")
            print(cowin_utility.colored(0, 255, 0, s.indirect(choice)))
        except KeyboardInterrupt:
            print(cowin_utility.colored(0, 255, 0, "\n\nKeyboard interrupt exception caught, Exiting ..\n\n"))
            sys.exit(0)

    print(cowin_utility.colored(0, 255, 255, '\nLoop ended. Thanks!\n'))  

if __name__ == "__main__":
    main()