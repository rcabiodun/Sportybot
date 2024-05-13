from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from  selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import pymongo
from selenium.webdriver.common.by import By
#this is to store previous meetings data in spare mongodb

myclient = pymongo.MongoClient("mongodb+srv://rcabiodun03:hflIAoElCc7hbMYn@cluster0.epr9vct.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

dblist = myclient.list_database_names()
print(dblist)
mydb = myclient["sporty"]
Matches = mydb["matches"]

betslip_count_limit=50
betslip_count=0
service=Service(executable_path="chromedriver.exe")
driver=webdriver.Chrome(service=service)

driver.get("https://livescores.biz/tomorrow")

WebDriverWait(driver,10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR,".item.match-grid-item"))
)

ans=0

game_elements=driver.find_elements(By.CSS_SELECTOR,".item.match-grid-item")
print(len(game_elements))
match_details=[]
match_count=0
for game in game_elements:
    if match_count>=1000:
        break
    match_title=game.find_element(By.CLASS_NAME,"match-grid-title")
    try:
        h2hBtn=game.find_element(By.CSS_SELECTOR,".label_link.h2h")
        match_details.append({"title":match_title.text,"link":h2hBtn.get_attribute("href")})
        match_count+=1
    except:
        print("Skipping game...no H2H")

# match_details=match_details[490:]
print(len(match_details))

for match_detail in match_details:

    print(match_detail["title"])

    h2hUrl=match_detail["link"]
    print(f"Heading to {h2hUrl}")
    try:
    
        service2=Service(executable_path="chromedriver.exe")

        driver2=webdriver.Chrome(service=service2)
        driver2.get(h2hUrl)


        WebDriverWait(driver2,10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,".table-block.last-matches"))
        )
        last_matches_elements=driver2.find_elements(By.CSS_SELECTOR,".table-block.last-matches")
        print(len(last_matches_elements))

        if len(last_matches_elements)==3:
            H2H_matches=last_matches_elements[0]
            scores=H2H_matches.find_elements(By.CSS_SELECTOR,".last-matches__score.col")
            scores_list=[]
            score_count=0
            for score in scores:
                if len(score.get_attribute("textContent"))>0:
                    if score_count==5:
                        break
                    score_line=score.get_attribute("textContent")
                    scores_list.append(score_line.strip())
                    score_count+=1
            
            data={"title":match_detail["title"],"scores":scores_list}
            x = Matches.insert_one(data)
        driver2.quit()
    except:

        print(f"skipping current game {match_detail['title']}")
        continue

print("done")
