from selenium.webdriver.common.by import By
import pymongo
from selenium.webdriver.common.by import By


myclient = pymongo.MongoClient("mongodb+srv://rcabiodun03:hflIAoElCc7hbMYn@cluster0.epr9vct.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
mydb = myclient["sporty"]
Matches = mydb["matches"]

dblist = myclient.list_database_names()



def checking_for_over_and_under(bet_choices,over_predictions=[],under_predictions=[],file=None):
    over_btns=[]
    under_btns=[]
    over_prediction_odds=0
    under_prediction_odds=0
    
    for bet_choice in bet_choices:
        if(bet_choice.find_element(By.CLASS_NAME,"m-table-header-title").text=="Over/Under"):
            over_and_under_elements= bet_choice.find_elements(By.CLASS_NAME,"m-table-cell-item")
            over_btns=bet_choice.find_elements(By.CSS_SELECTOR,".m-table-cell.m-table-cell--responsive")
            over_elements=over_and_under_elements[:2]
            prediction=over_predictions[0]-1
            if prediction<=0.5:
                #Since the prediction for over is 0.5-1...it would be better to just pick under
                file.write("It would be safer to pick under here. \n")
                over_prediction_odds=500
                break
            
            if str(prediction) in over_elements[0].text:
                file.write(f"This game can be carried {over_elements[0].text} at {over_elements[1].text} odds.\n")
                over_prediction_odds=over_elements[1].text
                break


    for bet_choice in bet_choices:
        if(bet_choice.find_element(By.CLASS_NAME,"m-table-header-title").text=="Over/Under"):
            over_and_under_elements= bet_choice.find_elements(By.CLASS_NAME,"m-table-cell-item")
            under_btns=bet_choice.find_elements(By.CSS_SELECTOR,".m-table-cell.m-table-cell--responsive")
            under_elements=over_and_under_elements[2:]
            prediction=under_predictions[0]+1#      
            if str(prediction) in under_elements[0].text:
                file.write(f"This game can be carried {under_elements[0].text} at {under_elements[1].text} odds. \n")
                under_prediction_odds=under_elements[1].text
                break

    
    if (float(over_prediction_odds)<float(under_prediction_odds)) and over_prediction_odds!=0:
        #Always choose the one with the lower odds expect of the odds is equal to zero
        file.write("Picked 'Over' \n")
        over_btns[2].click()
        return True

    elif float(under_prediction_odds)<float(over_prediction_odds)  and under_prediction_odds!=0:
       #Always choose the one with the lower odds expect of the odds is equal to zero
        file.write("Picked 'Under' \n")
        
        under_btns[3].click()
        return True
    elif(float(over_prediction_odds)>float(under_prediction_odds)) and over_prediction_odds==0:
        file.write("Picked 'Over' \n")

        over_btns[2].click()
        return True
    else:
        file.write("SKIPPING....WILL COME BACK TO THIS. \n")

        return False


def checking_for_handicap(bet_choices,averageGD,file=None):
   
    home_handicap_odds=0
    home_handicap_btn=None
    home_handicap_present=False
    away_handicap_present=False
    away_handicap_odds=0
    away_handicap_btn=None
    averageGD+=1
    
    for bet_choice in bet_choices:
        if(bet_choice.find_element(By.CLASS_NAME,"m-table-header-title").text==f"Handicap {averageGD}:0"):
            home_handicap_present=True
            #print(bet_choice.find_element(By.CLASS_NAME,"m-table-header-title").text)
            home_handicap_btn= bet_choice.find_elements(By.CSS_SELECTOR,".m-table-cell.m-table-cell--responsive")[2]
            home_handicap_odds= bet_choice.find_elements(By.CLASS_NAME,"m-table-cell-item")[1].text
            break

    for bet_choice in bet_choices:
        if(bet_choice.find_element(By.CLASS_NAME,"m-table-header-title").text==f"Handicap 0:{averageGD}"):
            away_handicap_present=True
            #print(bet_choice.find_element(By.CLASS_NAME,"m-table-header-title").text)
            away_handicap_btn= bet_choice.find_elements(By.CSS_SELECTOR,".m-table-cell.m-table-cell--responsive")[4]
            away_handicap_odds= bet_choice.find_elements(By.CLASS_NAME,"m-table-cell-item")[5].text
            break
    

      
    file.write(f"Home handicap odds at {averageGD}:0 is {home_handicap_odds} \n")
    file.write(f"Away handicap odds at 0:{averageGD} is {away_handicap_odds} \n")

    if home_handicap_present and away_handicap_present:
        if home_handicap_odds<away_handicap_odds:
            file.write("Going for home \n")       
            home_handicap_btn.click()
            return True
        else:
            file.write("Going for away \n")       
            away_handicap_btn.click()
            return True


    elif home_handicap_present and away_handicap_present==False:
        file.write("Going for home \n")       
        home_handicap_btn.click()
        return True

    elif away_handicap_present and home_handicap_present==False:
        file.write("Going for away \n")       
        away_handicap_btn.click()
        return True
    
    file.write("SKIPPING....WILL COME BACK TO THIS. \n")
    return False

  
          
          


def checking_double_chance(bet_choices,homeWins=[],awayWins=[],teamNames=[],team_forms=[],file=None):
    home_points=0
    away_points=0

    if int(homeWins[0]) > int(awayWins[0]):
        home_points+=1
    elif int(awayWins[0]) > int(homeWins[0]):
        away_points+=1
    else:
        home_points+=1
        away_points+=1
    
    if int(homeWins[1]) > int(awayWins[1]):
        home_points+=1
    elif int(awayWins[1]) > int(homeWins[1]):
        away_points+=1
    else:
        home_points+=1
        away_points+=1
    
    if int(team_forms[0])>int(team_forms[1]):
        home_points+=1.5
    elif int(team_forms[1])>int(team_forms[0]):
        away_points+=1.5

    else:
        home_points+=1.5
        away_points+=1.5


    file.write(f"Result from Decision engine --> Home points = {home_points} Away points = {away_points} \n")

    for bet_choice in bet_choices:
        if(bet_choice.find_element(By.CLASS_NAME,"m-table-header-title").text=="Double Chance"):
            if home_points>away_points:
                file.write("\t picking draw or home \n")
                bet_choice.find_elements(By.CSS_SELECTOR,".m-table-cell.m-table-cell--responsive")[2].click()
                return True
            if home_points<away_points:
                file.write ("\t picking draw or away \n")
                bet_choice.find_elements(By.CSS_SELECTOR,".m-table-cell.m-table-cell--responsive")[4].click()
                return True
            else:
                file.write("SKIPPING....WILL COME BACK TO THIS. \n")
                return False
       




def predict_over_and_under_threshold(average_goals_per_game):
    over_prediction = []
    under_prediction =[]
    
    if average_goals_per_game >=5 :
        over_prediction = [4.5,3.5,2.5,1.5,0.5]
    elif  average_goals_per_game >=4:
        over_prediction = [3.5,2.5,1.5,0.5]

    elif  average_goals_per_game >=3:
        over_prediction = [2.5,1.5,0.5]

    elif  average_goals_per_game >=2:
        over_prediction = [1.5,0.5]

    elif  average_goals_per_game >=1:
        over_prediction =[0.5] 

    
    if  average_goals_per_game >= 3.6 and average_goals_per_game<=4.5:
        under_prediction = [5.5,4.5,3.5,2.5]
    if  average_goals_per_game >= 3 and average_goals_per_game<=3.5:
        under_prediction = [4.5,3.5,2.5,1.5]
    elif  average_goals_per_game  >= 2 and average_goals_per_game<=3:
        under_prediction =[3.5,2.5,1.5,0.5]
    elif  average_goals_per_game  >= 1 and average_goals_per_game<=2:
        under_prediction = [2.5,1.5,0.5]
    elif  average_goals_per_game  >= 0 and average_goals_per_game<=1:
        under_prediction = [1.5,0.5]
    
    
    # new_over_prediction=over_prediction.copy()
    # new_under_prediction=under_prediction.copy()
  
    # if (risky==3):
    #     new_over_prediction=[]
    #     result=over_prediction[0]+1
    #     new_over_prediction.append(result)
    #     new_over_prediction.extend(over_prediction)
        
        
    #     if len(under_prediction)>1:
    #         new_under_prediction=under_prediction[1:]
    #     return new_over_prediction,new_under_prediction

    # elif(risky==2):
    #     return over_prediction,under_prediction

    # else:
    #     if len(over_prediction)>1:
    #         new_over_prediction=over_prediction[1:]
    #     return new_over_prediction,new_under_prediction
    return over_prediction,under_prediction

def check_db(team_names,file):
    #function to check if a particular game is already stored in the db
    in_db=False
    over_predictions,under_predictions=[],[]
    previous_meetings_avg_GD=0
    for matches in Matches.find():
        
        matchTitle=matches["title"]
        if team_names[0] in matchTitle and team_names[1] in matchTitle:
           # print(matches["scores"])
            in_db=True
            file.write("Game History is present in the Database \n")
            average_goals_per_game = getAverageGoalsPerGame(matches["scores"])
            

            over_predictions,under_predictions=predict_over_and_under_threshold(average_goals_per_game)
            previous_meetings_avg_GD=getAverageGoalDifferencePerGame(matches["scores"])

            file.write("From this game history i have concluded that: \n")
            file.write(f"\t Average goals score per game between their previous meetings is -->{average_goals_per_game} \n")
            file.write(f"\t Average goal difference  between their previous meetings is -->{previous_meetings_avg_GD} \n")
        

            #print(f"OVer and Under choices should be f{over_predictions,under_predictions}")
    
    if len(over_predictions)>0:
        file.write(f"This game can be carried on the following 'Overs': \n")
        for over_prediction in over_predictions:
            file.write(f"\t Over {over_prediction} \n")

        
    if len(under_predictions)>0:
        file.write(f"This game can be carried on the following 'Unders': \n")
        for under_prediction in under_predictions:
            file.write(f"\t Under {under_prediction} \n")


    #print(f"in_db --> {in_db}")
    return in_db,over_predictions,under_predictions,previous_meetings_avg_GD

def check_db_dummy(team_names):
    #function to check if a particular game is already stored in the db
    in_db=True
    over_predictions,under_predictions=[3.5,2.5],[4.5,3.5]
    previous_meetings_avg_GD=2
    return in_db,over_predictions,under_predictions,previous_meetings_avg_GD

def getAverageGoalsPerGame(score_lines):
    total_goals = 0
    num_games = len(score_lines)
    for score in score_lines:
        home_goals, away_goals = map(int, score.split('-'))
        total_goals += home_goals + away_goals
    average_goals_per_game = total_goals / num_games
   # print(f"Average goals per game is {average_goals_per_game}")
    return average_goals_per_game

def getAverageGoalDifferencePerGame(score_lines):
    total_goals = 0
    num_games = len(score_lines)
    for score in score_lines:
        home_goals, away_goals = map(int, score.split('-'))
        result=0
        if home_goals >away_goals:
            result=home_goals-away_goals
        else:
            result=away_goals-home_goals
        total_goals += result
    average_goals_per_game = total_goals / num_games
    #print(f"Average goal difference between pevious meetings is {average_goals_per_game.__ceil__()}")
    return average_goals_per_game.__ceil__()

    # Use the average goals per game to make predictions



class colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'  
# Example usage:


# # import requests
# # page=requests.get("https://livescores.biz/tomorrow#today-cookie")

# # print(page.text)
# for i in range(len(x)):
#     print(i)