from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from  selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
from utils import *
import random
import requests
import pyfiglet
# Define the URL of your API endpoint
from tqdm import tqdm
import time
from webdriver_manager.chrome import ChromeDriverManager

LOCAL_VERSION=1.0
# Define the total number of iterations


# Create a tqdm instance with the total number of iterations


# Simulate some task that progresses


def Bot(number_of_available_games):
    welcome_text="Hi, i'm Betbot!"
    ascii_art = pyfiglet.figlet_format(welcome_text)

    # #print ASCII art
    print(ascii_art)

    is_booting=True
    slip_limit=0
    while is_booting:
        code=input("If you're opting for the paid tier kindly type in the code sent to your mail verifying your subscription or if you want to use the free trial press 'n' ")
        if code.lower() =="n":
            slip_limit=40
            print(colors.YELLOW + f"Free trial is limited to only {slip_limit} games per slip.Head to our website to complete subscribe for our paid plan at https://bet-b0t.onrender.com " + colors.RESET)
            is_booting=False
            break

        url = 'https://bet-b0t.onrender.com/verify_code'

        # Define the data you want to send
        data = {
            'code': code,
        }
        # Send a POST request with the data to the API endpoint
        try:
            response = requests.post(url, json=data)
        except:
            print(colors.RED + f"Kindly check your internet connection" + colors.RESET)
        # Check the response status code
        if response.status_code == 200:
            version=response.json()["current_version"]
            if LOCAL_VERSION !=version:

                print(colors.YELLOW + "An update is now available.Kindly head to our website to download the new version of the program and delete this 🙃" + colors.RESET)
                time.sleep(5)
                exit()
            
            while True:
                slip_limit = int(input("Enter a number (not more than 45 and at least 10 less than available matches): "))
                if slip_limit <= 45 and (number_of_available_games - slip_limit) >= 10:
                    break
                else:
                    print(colors.RED +"Invalid input! Please enter a number that is not more than 45 and at least 10 less than available matches." + colors.RESET)

            is_booting=False

        elif response.status_code == 400:
            print(colors.YELLOW + f"Your plan has expired...You can press 'n' to proceed to the free trial of resubscribe to the paid tier from our site." + colors.RESET)
        else:
            print(colors.RED + f"Code inputed is invalid" + colors.RESET)



    GAME_CHOICES=["Handicap","Double Chance","Over/Under"]

    # Your array


    # Choose a random element from the array
    betslip_count_limit=int(slip_limit)
    betslip_count=0
    service=Service("chromedriver.exe")
    driver=webdriver.Chrome(service=service)

    driver.get("https://www.sportybet.com/ng/sport/football/upcoming?time=24")


    WebDriverWait(driver,60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,".m-table-row.m-content-row.match-row"))
    )


    match_rows = driver.find_elements(By.CSS_SELECTOR, ".m-table-row.m-content-row.match-row")
    #print(f"found {len(match_rows)} matches on the first page")
    page=2
    visited_games=[]
    progress_bar = tqdm(total=slip_limit, desc="Progress", unit="iteration")
    file_name = "analysisq.txt"
    with open(file_name, "w") as file:
    # Write some content to the file
        
        while betslip_count <betslip_count_limit:
            try:
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".m-table-row.m-content-row.match-row")))
            
                page=2
                matches = driver.find_elements(By.CSS_SELECTOR, ".m-table-row.m-content-row.match-row")
                match = random.choice(matches)
                home_odds = match.find_element(By.CLASS_NAME, "m-outcome-odds")
                stats = match.find_element(By.CLASS_NAME, "lmt-icon")

                stats.click()
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".sr-tabs-tab__wrapper.srct-tab.srm-is-fullwidth")))
                
                team_names_elements = driver.find_elements(By.CLASS_NAME, "sr-lmt-plus-scb__team-name")
                team_name=[]
                for name in team_names_elements:
                    
                    team_name.append(name.text)
                
                # print(team_name)
                # WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".sr-tabs-tab__wrapper.srct-tab.srm-is-fullwidth")))
                
                H_H = driver.find_elements(By.CSS_SELECTOR, ".sr-tabs-tab__wrapper.srct-tab.srm-is-fullwidth")

                # print(len(H_H))
                H_H=H_H[1]

                H_H.click()


                #here try to get home and away wins against each other
                # WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "sr-lmt-0-ms-league-position-form__form-label-value")))
                team_forms_elements = None

                WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".sr-lmt-plus-slidetitle__title.srt-text-secondary.srm-no-border.srm-is-uppercase")))
                
                away_form_element = driver.find_element(By.CSS_SELECTOR, ".sr-lmt-plus-0-meetingsandform__fc-value.srt-base-1-away-1").text
                home_form_element = driver.find_element(By.CSS_SELECTOR, ".sr-lmt-plus-0-meetingsandform__fc-value.srt-base-1-home-1").text
                # print(away_form_element)
                # print(home_form_element)
                previous_meeting_element=driver.find_elements(By.CSS_SELECTOR, ".sr-lmt-plus-slidetitle__title.srt-text-secondary.srm-no-border.srm-is-uppercase")
                #print(len(previous_meeting_element))
                if previous_meeting_element[1].text == "PREVIOUS MEETINGS" or previous_meeting_element[0].text == "PREVIOUS MEETINGS" :
                    # previous_meeting_home_wins=match.find_element(By.CLASS_NAME, "sr-previous-meetings-graph__numbers").text
                    previous_meeting_home_wins=driver.find_elements(By.CSS_SELECTOR, ".sr-previous-meetings-graph__numbers-label.srt-base-1-home-1.srm-is-transparent")
                    previous_meeting_away_wins=driver.find_elements(By.CSS_SELECTOR, ".sr-previous-meetings-graph__numbers-label.srt-base-1-away-1.srm-is-transparent")

                    # headers=driver.find_element(By.CSS_SELECTOR, ".sr-previous-meetings-graph__numbers-label.srt-base-1-home-1.srm-is-transparent")
                else:
                    #if there are no previos meetings...go to the next match
                    continue

                meeting_home_wins=[]
                meeting_away_wins=[]
                team_forms=[]
                #print(f"len of team for elements {len(team_forms_elements)}")

                if len(away_form_element.strip())>0 and len(home_form_element.strip())>0:
                    team_forms.append(home_form_element)                
                    team_forms.append(away_form_element)

                else:
                    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "sr-lmt-0-ms-league-position-form__form-label-value")))
                    team_forms_elements = driver.find_elements(By.CLASS_NAME, "sr-lmt-0-ms-league-position-form__form-label-value")
                    for i in range(2):
                        team_forms.append(team_forms_elements[i].get_attribute("textContent"))

                
                for i in range(2):
                    meeting_away_wins.append(previous_meeting_away_wins[i].get_attribute("textContent"))
                    meeting_home_wins.append(previous_meeting_home_wins[i].get_attribute("textContent"))

                if team_name in visited_games:
                    #print("Oops...picked an already visited game")
                    continue
                
                file.write(f"Home Team --> {team_name[0]}. \n")
                file.write(f"\tTotal Meetings Win --> {meeting_home_wins[0]}, Last Five Meeting Wins --> {meeting_home_wins[1]}, Their From At the moment is --> {team_forms[0]}%. \n")

                file.write(f"Away Team --> {team_name[1]}. \n")
                file.write(f"\tTotal Meetings Win --> {meeting_away_wins[0]}, Last Five Meeting Wins --> {meeting_away_wins[1]},Their From At the moment is --> {team_forms[1]}%.\n")

                
                

            

                team_in_db,over_predictions,under_predictions,averageGD=check_db(team_names=team_name,file=file)
                stats.click()
                
                # #print(f"The form of the teams are {team_forms}")
                if betslip_count == betslip_count_limit:
                    break
                else:
                    link = match.find_element(By.CSS_SELECTOR, ".m-table-cell.market-size")
                    link.click()
                    page=3
                    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "m-table__wrapper")))

                    bet_choices=driver.find_elements(By.CLASS_NAME,"m-table__wrapper")

                    random_element = random.choice(GAME_CHOICES)
                    
                    #print(f"Rnadomly chose {random_element}")
                
                    if team_in_db and random_element =="Over/Under":
                        #print("Trying to stake Over/Under")
                        added_to_slip=checking_for_over_and_under(bet_choices,over_predictions,under_predictions,file)
                        if added_to_slip:
                            if len(team_name) >0:
                                visited_games.append(team_name)
                            betslip_count += 1
                            progress_bar.update(1)
                            file.write("ADDED TO SLIP \n")

                    elif team_in_db  and random_element =="Handicap":
                        added_to_slip=checking_for_handicap(bet_choices,averageGD,file)
                        if added_to_slip:
                            if len(team_name) >0:
                                visited_games.append(team_name)
                            betslip_count += 1
                            progress_bar.update(1)
                            file.write("ADDED TO SLIP \n")
                    else:
                        #print("Trying to stake a Db chance")
                        added_to_slip= checking_double_chance(bet_choices,meeting_home_wins,meeting_away_wins,team_name,team_forms,file)
                        if added_to_slip:
                            if len(team_name) >0:
                                visited_games.append(team_name)
                            betslip_count += 1
                            progress_bar.update(1)
                            file.write("ADDED TO SLIP \n")
                    driver.back()

                    #print(f"Have {betslip_count} games in the slip")
                    file.write("\n")

                    file.write("---------------------------------------------------------------------------------------------------------------------------------------------------------------")
                    file.write("\n")
            except Exception as e:
                if(page==3):
                    driver.back()
                    continue
                else:
                    continue
        file.close()
        progress_bar.close()
        print("Done boss ")
        print("You can kindly edit the games now ...Check the analysis.txt file to view the breakdown of what went down")
        print(colors.RED + f"Closing me will close the browser...so kindly place your bet before closing me" + colors.RESET)
        time.sleep(45000)


service=Service("chromedriver.exe")
driver=webdriver.Chrome(service=service)
driver.get("https://www.sportybet.com/ng/sport/football/upcoming?time=24")


    # WebDriverWait(driver,40).until(
    #     EC.presence_of_element_located((By.CLASS_NAME,"top-link"))
    # )


    # todays_football=driver.find_element(By.CLASS_NAME,"top-link")
    # todays_football.click()

WebDriverWait(driver,60).until(
    EC.presence_of_element_located((By.CSS_SELECTOR,".m-table-row.m-content-row.match-row"))
)


match_rows = driver.find_elements(By.CSS_SELECTOR, ".m-table-row.m-content-row.match-row")
print(colors.YELLOW + f"found {len(match_rows)} matches on the first page" + colors.RESET)
driver.close()
MATCHES=len(match_rows)
counter=0
while counter<5:
    Bot(MATCHES)
    counter=counter+1