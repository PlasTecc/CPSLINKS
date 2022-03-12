import os
import json
import webbrowser
import requests
import pyperclip
from time import sleep
from datetime import datetime as date
from tabulate import tabulate


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    OKWHITE = '\033[97m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


appdata = os.getenv('APPDATA')

try:
    selected_key = json.load(open(f"{appdata}\\data.json", "rb"))["key"]
    classroom = json.load(open(f"{appdata}\\data.json", "rb"))["classroom"]
except FileNotFoundError:
    json_data = {"key": "key_here", "timetable": {},
                 "zoomlinks": {}, "classroom": "classroom_here"}
    with open(f"{appdata}\\data.json", "w") as outfile:
        json.dump(json_data, outfile)
    selected_key = json.load(open(f"{appdata}\\data.json", "rb"))["key"]
    classroom = json.load(open(f"{appdata}\\data.json", "rb"))["classroom"]

current_day = date.today().strftime("%A")
api_key = "api_key_here"
api_url = "https://api.jsonbin.io/v3/b/"
api_header = {"X-Master-Key": api_key}


def banner():
    banner = f"""{bcolors.OKWHITE}
█████████████████████████████████████████
█─▄▄▄─█▄─▄▄─█─▄▄▄▄█─▄─▄─█─▄▄─█─▄▄─█▄─▄███
█─███▀██─▄▄▄█▄▄▄▄─███─███─██─█─██─██─██▀█
▀▄▄▄▄▄▀▄▄▄▀▀▀▄▄▄▄▄▀▀▄▄▄▀▀▄▄▄▄▀▄▄▄▄▀▄▄▄▄▄▀ PlasTec#5267 | V2.0 | {selected_key} | {classroom}
"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(banner)


timetable = json.load(open(f"{appdata}\\data.json", "rb"))["timetable"]
zoomlinks = json.load(open(f"{appdata}\\data.json", "rb"))["zoomlinks"]


def mainMenu():
    try:
        banner()
        print("0. EXIT")
        print("1. JOIN MEETING")
        print("2. CREATE TIMETABLE")
        print("3. EDIT KEY")
        print("4. VIEW CURRENT SELECTED TIMETABLE")
        user_input = input("> ")
        if 0 <= int(user_input) <= 4:
            if int(user_input) == 0:
                endMenu()
            if int(user_input) == 1:
                joinMenu()
            if int(user_input) == 2:
                createMenu()
            if int(user_input) == 3:
                keyMenu()
            if int(user_input) == 4:
                viewMenu()
        else:
            raise ValueError
    except ValueError:
        print(f"{bcolors.FAIL}INVALID INPUT!{bcolors.ENDC}")
        if input(f"{bcolors.WARNING}WOULD YOU LIKE TO TRY AGAIN? (Y/N): {bcolors.ENDC}").upper() == "Y":
            mainMenu()
        else:
            endMenu()


def joinMenu():
    banner()
    if selected_key:
        if current_day != "Friday" and current_day != "Saturday":
            currentday_timetable = timetable[current_day]
            for subject in currentday_timetable:
                print(f"{currentday_timetable.index(subject) + 1}. {subject}")
            subject_input = input("> ")
            try:
                if int(subject_input) > 0:
                    subject_index = int(subject_input) - 1
                    zoomlink = zoomlinks[currentday_timetable[subject_index]]
                    if len(zoomlink) >= 30:
                        webbrowser.open(zoomlink)
                        if input(f"{bcolors.WARNING}WOULD YOU LIKE TO TRY AGAIN? (Y/N): {bcolors.ENDC}").upper() == "Y":
                            joinMenu()
                        else:
                            mainMenu()
                    else:
                        print(f"{bcolors.FAIL}CHECK WHATSAPP!{bcolors.ENDC}")
                        if input(f"{bcolors.WARNING}WOULD YOU LIKE TO TRY AGAIN? (Y/N): {bcolors.ENDC}").upper() == "Y":
                            joinMenu()
                        else:
                            mainMenu()
                else:
                    raise Exception
            except Exception:
                print(f"{bcolors.FAIL}INVALID CHOICE!{bcolors.ENDC}")
                if input(f"{bcolors.WARNING}WOULD YOU LIKE TO TRY AGAIN? (Y/N): {bcolors.ENDC}").upper() == "Y":
                    joinMenu()
                else:
                    mainMenu()
        else:
            print(f"{bcolors.FAIL}THERE IS NO SCHOOL TODAY!{bcolors.ENDC}")
            input(f"{bcolors.WARNING}PRESS ENTER TO GO...{bcolors.ENDC}")
            mainMenu()
    else:
        print(f"{bcolors.FAIL}PLEASE INPUT A KEY!{bcolors.ENDC}")
        input(f"{bcolors.WARNING}PRESS ENTER TO GO BACK...{bcolors.ENDC}")
        mainMenu()


def createMenu():
    banner()
    while True:
        new_classroom = input("CLASSROOM: ")
        new_data = {"timetable": {"Sunday": [], "Monday": [], "Tuesday": [],
                                  "Wednesday": [], "Thursday": []}, "zoomlinks": {}, "classroom": new_classroom}
        for day in new_data["timetable"]:
            banner()
            print(f"{day}: ")
            count = 1
            while count <= 8:
                subject = input(f"Period {count}: ").upper()
                if subject:
                    new_data["timetable"][day].append(subject)
                    count += 1
                else:
                    count = 1
                    break
        banner()
        tabulate_header = ["", "1", "2", "3", "4", "5", "6", "7", "8"]
        tabulate_timetable = [[], [], [], [], []]
        index = 0
        for day in new_data["timetable"]:
            tabulate_timetable[index].append(day)
            for subject in new_data["timetable"][day]:
                tabulate_timetable[index].append(subject)
            index += 1
        print(tabulate(tabulate_timetable, headers=tabulate_header))
        if input(f"{bcolors.WARNING}DO YOU LIKE IT? (Y/N): {bcolors.ENDC}").upper() == "Y":
            break
        else:
            if input(f"{bcolors.WARNING}WOULD YOU LIKE TO TRY AGAIN? (Y/N): {bcolors.ENDC}").upper() == "N":
                mainMenu()

    allsubjects = []
    for day in new_data["timetable"]:
        allsubjects += new_data["timetable"][day]
    allsubjects = sorted(list(dict.fromkeys(allsubjects)))

    while True:
        for subject in allsubjects:
            while True:
                banner()
                print(
                    f"{bcolors.WARNING}LEAVE INPUT EMPTY FOR SUBJECTS LIKE GH!{bcolors.ENDC}")
                zoom_code = input(f"{subject}: https://cpsbahrain.zoom.us/j/")
                if len(zoom_code) >= 9 and zoom_code.isdecimal():
                    new_data["zoomlinks"][subject] = f"https://cpsbahrain.zoom.us/j/{zoom_code}"
                    break
                elif zoom_code == "":
                    new_data["zoomlinks"][subject] = f"https://cpsbahrain.zoom.us/j/{zoom_code}"
                    break
                else:
                    print(f"{bcolors.WARNING}INVALID CODE!{bcolors.ENDC}")
                    input(f"{bcolors.FAIL}PRESS ENTER TO RETRY...{bcolors.ENDC}")

        tabulate_zoomlink = []

        for subject in new_data["zoomlinks"]:
            tabulate_zoomlink.append([subject, new_data["zoomlinks"][subject]])

        banner()
        print(tabulate(tabulate_zoomlink))
        if input(f"{bcolors.WARNING}DO YOU LIKE IT? (Y/N): {bcolors.ENDC}").upper() == "Y":
            break
        else:
            if input(f"{bcolors.WARNING}WOULD YOU LIKE TO TRY AGAIN? (Y/N): {bcolors.ENDC}").upper() == "N":
                mainMenu()

    while True:
        api_header["Content-Type"] = "application/json"
        r = requests.post(api_url, json=new_data, headers=api_header)
        if r.status_code == 200:
            new_key = r.json()["metadata"]["id"]
            print(f"{bcolors.OKGREEN}Your key is: {new_key}{bcolors.ENDC}")
            pyperclip.copy(new_key)
            api_header.pop("Content-Type")
            input(f"{bcolors.WARNING}PRESS ENTER TO GO BACK...{bcolors.ENDC}")
            break
        else:
            print(f"{bcolors.FAIL}FAILED TO CREATE KEY!{bcolors.ENDC}")
            if input(f"{bcolors.WARNING}WOULD YOU LIKE TO TRY AGAIN? (Y/N): {bcolors.ENDC}").upper() == "N":
                break

    mainMenu()


def keyMenu():
    try:
        banner()
        key_input = input("KEY: ")
        if input(f"{bcolors.WARNING}ARE YOU SURE THIS IS THE CORRECT KEY? (Y/N): {bcolors.ENDC}").upper() == "Y":
            if len(key_input) >= 24 and key_input.isalnum():
                r = requests.get(api_url+key_input, json=None,
                                 headers=api_header)
                if r.status_code == 200:
                    data = r.json()
                    data_json = {
                        "key": key_input,
                        "timetable": data["record"]["timetable"],
                        "zoomlinks": data["record"]["zoomlinks"],
                        "classroom": data["record"]["classroom"]
                    }
                    with open(f"{appdata}\\data.json", "w") as outfile:
                        json.dump(data_json, outfile)
                    global selected_key
                    global timetable
                    global zoomlinks
                    global classroom
                    selected_key = key_input
                    timetable = json.load(open(f"{appdata}\\data.json", "rb"))[
                        "timetable"]
                    zoomlinks = json.load(open(f"{appdata}\\data.json", "rb"))[
                        "zoomlinks"]
                    classroom = json.load(open(f"{appdata}\\data.json", "rb"))[
                        "classroom"]
                    print(f"{bcolors.OKGREEN}CHANGED KEY!{bcolors.ENDC}")
                    input(
                        f"{bcolors.WARNING}PRESS ENTER TO GO BACK...{bcolors.ENDC}")
                    mainMenu()
                else:
                    raise Exception
            else:
                raise Exception
        else:
            if input(f"{bcolors.WARNING}WOULD YOU LIKE TO TRY AGAIN? (Y/N): {bcolors.ENDC}").upper() == "Y":
                keyMenu()
            else:
                mainMenu()
    except Exception:
        print(f"{bcolors.FAIL}INVALID KEY!{bcolors.ENDC}")
        if input(f"{bcolors.WARNING}WOULD YOU LIKE TO TRY AGAIN? (Y/N): {bcolors.ENDC}").upper() == "Y":
            keyMenu()
        else:
            mainMenu()


def viewMenu():
    banner()
    if selected_key:
        tabulate_header = ["", "1", "2", "3", "4", "5", "6", "7", "8"]
        tabulate_timetable = [[], [], [], [], []]
        index = 0
        for day in timetable:
            tabulate_timetable[index].append(day)
            for subject in timetable[day]:
                tabulate_timetable[index].append(subject)
            index += 1
        print(tabulate(tabulate_timetable, headers=tabulate_header))

        all_links = []
        for name in zoomlinks:
            all_links.append([name+":", zoomlinks[name]])
        print(tabulate(all_links))

        input(f"{bcolors.WARNING}PRESS ENTER TO GO BACK...{bcolors.ENDC}")
        mainMenu()
    else:
        print(f"{bcolors.FAIL}PLEASE INPUT A KEY!{bcolors.ENDC}")
        input(f"{bcolors.WARNING}PRESS ENTER TO GO BACK...{bcolors.ENDC}")
        mainMenu()


def endMenu(timer=3):
    for i in range(timer, 0, -1):
        banner()
        print(
            f"Thanks for using CPSTOOL developed by PlasTec. Exiting in {i} seconds...")
        sleep(1)
    exit()


mainMenu()
