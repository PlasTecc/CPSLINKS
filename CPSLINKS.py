import calendar
import datetime
import requests
import webbrowser
import time
import os

zoom_links_json_url = "https://raw.githubusercontent.com/PlasTecc/CPSLINKS/main/links.json"
timetable_json_url = "https://raw.githubusercontent.com/PlasTecc/CPSLINKS/main/timetable.json"
current_day = calendar.day_name[datetime.date.today().weekday()]
banner = f"""   ____ ____  ____  _     ___ _   _ _  ______  
  / ___|  _ \/ ___|| |   |_ _| \ | | |/ / ___| 
 | |   | |_) \___ \| |    | ||  \| | ' /\___ \ 
 | |___|  __/ ___) | |___ | || |\  | . \ ___) |
  \____|_|   |____/|_____|___|_| \_|_|\_\____/ 
                                               By PlasTec#5267 | Version: 2.0 | 11A only."""

if current_day != "Friday" and current_day != "Saturday":
    print(banner)
    zoom_links = requests.get(zoom_links_json_url).json()
    timetable = requests.get(timetable_json_url).json()[current_day]
    while True:
        try:
            counter = 1
            os.system('cls' if os.name == 'nt' else 'clear')
            print(banner)
            for subject in timetable:
                print(f"{counter}. {subject}")
                counter += 1
            user_input = int(input("> "))
            subject_index = user_input - 1
            if user_input > 0:
                if timetable[subject_index] != "GH":
                    webbrowser.open(zoom_links[timetable[subject_index]])
                    if input("Would you like to use it again? (Y/N): ").lower() == "n":
                        break
                else:
                    input(
                        "Please check the whatsapp group for the link.\nPress Enter to continue...")
            else:
                if input("Invalid input!\nWould you like to try again? (Y/N): ").lower() == "n":
                    break

        except Exception:
            if input("Invalid input!\nWould you like to try again? (Y/N): ").lower() == "n":
                break
else:
    print(banner)
    input("There is no school today!\nPress Enter to continue...")


print("Thanks for using CPSLINKS developed by PlasTec. Exiting in 3 seconds...")
time.sleep(3)
