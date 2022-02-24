import calendar
import datetime
import requests
import webbrowser
import time
import os


links_json_url = "https://raw.githubusercontent.com/PlasTecc/PlasTecc/main/links.json"
timetable_json_url = "https://raw.githubusercontent.com/PlasTecc/PlasTecc/main/timetable.json"
version_json_url = "https://raw.githubusercontent.com/PlasTecc/PlasTecc/main/version.json"
current_date = calendar.day_name[datetime.date.today().weekday()]
links = requests.get(links_json_url).json()
timetable = requests.get(timetable_json_url).json()[current_date]
version = requests.get(version_json_url).json()["Version"]
banner = f"""   ____ ____  ____  _     ___ _   _ _  ______  
  / ___|  _ \/ ___|| |   |_ _| \ | | |/ / ___| 
 | |   | |_) \___ \| |    | ||  \| | ' /\___ \ 
 | |___|  __/ ___) | |___ | || |\  | . \ ___) |
  \____|_|   |____/|_____|___|_| \_|_|\_\____/ 
                                               By Ziyad Salah | Version: {version}"""


while True:
    try:
        if current_date != "Friday" or current_date != "Saturday":
            counter = 1
            print(banner)
            for subject in timetable:
                print(f"{counter}. {subject}")
                counter += 1
            my_choice = int(input("> "))
            if timetable[my_choice - 1] == "GH":
                print(
                    "There is no set link for the Golden Hour please check the whatsapp group for the link.")
            else:
                webbrowser.open(links[timetable[my_choice - 1]])
            con = input("Would you like to continue? (Y/N): ").lower()
            if con == "n":
                break
            os.system('cls' if os.name == 'nt' else 'clear')
        else:
            print("There is no school today!")
            break
    except ValueError:
        print("You have either entered letter or an invalid number!")
        answer = input("Would you like to try again? (Y/N): ").lower()
        if answer == "n":
            break

print("Thanks for using CPSLINKS developed by Ziyad. Exiting in 3 seconds...")
time.sleep(3)
