from datetime import date, datetime

from colorama import Fore, Back, Style
from colorama import init
from termcolor import colored

import os
import ctypes
from ctypes import wintypes
import msvcrt
import subprocess

ctypes.windll.kernel32.SetConsoleTitleW("Date Difference - Jam - 2022")
os.system('mode con: cols=100 lines=40')
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
user32 = ctypes.WinDLL('user32', use_last_error=True)

SW_MAXIMIZE = 3

kernel32.GetConsoleWindow.restype = wintypes.HWND
kernel32.GetLargestConsoleWindowSize.restype = wintypes._COORD
kernel32.GetLargestConsoleWindowSize.argtypes = (wintypes.HANDLE,)
user32.ShowWindow.argtypes = (wintypes.HWND, ctypes.c_int)

def maximize_console(lines=None):
    fd = os.open('CONOUT$', os.O_RDWR)
    try:
        hCon = msvcrt.get_osfhandle(fd)
        max_size = kernel32.GetLargestConsoleWindowSize(hCon)
        if max_size.X == 0 and max_size.Y == 0:
            raise ctypes.WinError(ctypes.get_last_error())
    finally:
        os.close(fd)
    cols = max_size.X
    hWnd = kernel32.GetConsoleWindow()
    if cols and hWnd:
        if lines is None:
            lines = max_size.Y
        else:
            lines = max(min(lines, 9999), max_size.Y)
        subprocess.check_call('mode.com con cols={} lines={}'.format(
                                cols, lines))
        user32.ShowWindow(hWnd, SW_MAXIMIZE)

maximize_console(lines=None)

init(autoreset=True)

global r
global g
global b
global w
global y
global c
global m
global bl

r = Fore.RED
g = Fore.GREEN
b = Fore.BLUE
w = Fore.WHITE
y = Fore.YELLOW
c = Fore.CYAN
m = Fore.MAGENTA
bl = Fore.BLACK

global rbg
global gbg
global bbg
global wbg
global ybg
global cbg
global mbg

rbg = Back.RED
gbg = Back.GREEN
bbg = Back.BLUE
wbg = Back.WHITE
ybg = Back.YELLOW
cbg = Back.CYAN
mbg = Back.MAGENTA

global bright
global dim

bright = Style.BRIGHT
dim = Style.DIM

def p(t, color):
    text = color + t
    return text

def bg(t, color):
    text = color + t
    return text

def sty(t, level):
    text = level + t
    return text

fix = '\033[0m'

print("")
print(sty(p(" Date Difference | by Jam | 2022", g), bright))
print("")
print(sty(p(" Dates should be entered in the format Month/Day/Year as numbers.", c), dim))
print(sty(p(" (Example -> 9/15/2002)", c), dim))
print("")

def get_difference(date1, date2):
    difference = date2 - date1
    return str(difference.days)

def add_number_suffix(number):

    digit = number[-1:]

    if digit == "0" or digit == "4" or digit == "5" or digit == "6" or digit == "7" or digit == "8" or digit == "9":
        return number+"th"
    elif digit == "1":
        return number+"st"
    elif digit == "2":
        return number+"nd"
    elif digit == "3":
        return number+"rd"

def process_data(data):

    firstSet = data[0].split("/")
    secondSet = data[1].split("/")

    while len(firstSet[2]) < 4:
        firstSet[2] = "0" + firstSet[2]

    while len(secondSet[2]) < 4:
        secondSet[2] = "0" + secondSet[2]

    firstDate = date(int(firstSet[2]), int(firstSet[0]), int(firstSet[1]))
    secondDate = date(int(secondSet[2]), int(secondSet[0]), int(secondSet[1]))

    dateDifference = get_difference(firstDate, secondDate)

    firstDaysNumber = date(int(firstSet[2]), int(firstSet[0]), int(firstSet[1])).timetuple().tm_yday
    secondDaysNumber = date(int(secondSet[2]), int(secondSet[0]), int(secondSet[1])).timetuple().tm_yday
 
    firstDaysSuffix = add_number_suffix(str(firstDaysNumber))
    secondDaysSuffix = add_number_suffix(str(secondDaysNumber))

    endOfYear1 = date(int(firstSet[2]),12,31).timetuple().tm_yday
    endOfYear2 = date(int(secondSet[2]),12,31).timetuple().tm_yday
    
    firstDifference = endOfYear1 - firstDaysNumber
    firstDaysLeft = str(firstDifference)

    secondDifference = endOfYear2 - secondDaysNumber
    secondDaysLeft = str(secondDifference)

    mirrorDays1 = str(firstDifference)
    mirrorDays2 = str(secondDifference)

    if mirrorDays1 == "0":
        mirrorDate1 = "None"
    else:
        mirrorDays1.rjust(3 + len(mirrorDays1), '0')
        mirrorDate1 = datetime.strptime(firstSet[2] + "-" + mirrorDays1, "%Y-%j").strftime("%m/%d/%Y")

    if mirrorDays2 == "0":
        mirrorDate2 =  "None"
    else:
        mirrorDays2.rjust(3 + len(mirrorDays2), '0')
        mirrorDate2 = datetime.strptime(secondSet[2] + "-" + mirrorDays2, "%Y-%j").strftime("%m/%d/%Y")

    print(" " + p(data[0] + ": ", b) + p(firstDaysSuffix + " day of the year with " + firstDaysLeft + " days left in the year.", c) + p(" Mirror Date: ", b) + p(mirrorDate1, c))
    print(" " + p(data[1] + ": ", b) + p(secondDaysSuffix + " day of the year with " + secondDaysLeft + " days left in the year.", c) + p(" Mirror Date: ", b) + p(mirrorDate2, c))
    if dateDifference == "1":
        print(" " + p("There is " + dateDifference + " day between ", c) + p(data[0], b) + p(" and ", c) + p(data[1], b) + p(".", b))
    else:
        print(" " + p("There is " + dateDifference + " days between ", c) + p(data[0], b) + p(" and ", c) + p(data[1], b) + p(".", b))
        
def main():
    
    up = True

    while up:
        print("-----------------------------------------------------------------------------------------------------------------------------------------------------")
        date1 = input(" Date 1: ")
        date1end = date1[-1:]
        date2 = input(" Date 2: ")
        data = [date1, date2]
        try:
            process_data(data)
        except:
            print(p(" Error occurred, likely due to incorrect format of input.", r))

main()
    
