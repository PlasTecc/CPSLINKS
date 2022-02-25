import calendar
import datetime
import requests
import webbrowser
import time
import os

links_json_url = "https://raw.githubusercontent.com/PlasTecc/CPSLINKS/main/links.json"
timetable_json_url = "https://raw.githubusercontent.com/PlasTecc/CPSLINKS/main/timetable.json"
current_date = calendar.day_name[datetime.date.today().weekday()]
links = requests.get(links_json_url).json()
timetable = requests.get(timetable_json_url).json()[current_date]
banner = f"""   ____ ____  ____  _     ___ _   _ _  ______  
  / ___|  _ \/ ___|| |   |_ _| \ | | |/ / ___| 
 | |   | |_) \___ \| |    | ||  \| | ' /\___ \ 
 | |___|  __/ ___) | |___ | || |\  | . \ ___) |
  \____|_|   |____/|_____|___|_| \_|_|\_\____/ 
                                               By PlasTec#5267 | Version: 1.0 | 11A only."""

while True:
    try:
        if current_date == "Friday" or current_date == "Saturday":
            print("There is no school today!")
            input("Press Enter to continue...")
            break
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            counter = 1
            print(banner)
            for subject in timetable:
                print(f"{counter}. {subject}")
                counter += 1
            my_choice = int(input("> "))
            if my_choice > 0:
                if timetable[my_choice - 1] == "GH":
                    print("Please check the whatsapp group for the link.")
                    input("Press Enter to continue...")
                else:
                    webbrowser.open(links[timetable[my_choice - 1]])
            else:
                print("You have either entered letter or an invalid number!")
            con = input("Would you like to continue? (Y/N): ").lower()
            if con == "n":
                break
    except Exception:
        print("You have either entered letter or an invalid number!")
        answer = input("Would you like to try again? (Y/N): ").lower()
        if answer == "n":
            break

print("Thanks for using CPSLINKS developed by PlasTec. Exiting in 3 seconds...")
time.sleep(3)
