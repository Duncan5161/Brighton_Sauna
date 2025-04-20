
from flask import Flask, request, render_template, redirect, url_for
import urllib.request 
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def index(): 

    return render_template("index.html")

@app.route("/quiz", methods=["GET", "POST"])
def quiz(): 

    saunadelic = 0
    luna = 0
    beach_box = 0

    if request.method == "POST":

        answer1 = request.form.get("Q1") #Q1 Near the sea
        if answer1 == "yes":
            luna += 1
            beach_box += 1 

        answer2 = request.form.get("Q2") #Q2 Ice balls on sauna
        if answer2 == "yes":
            saunadelic += 1

        answer3 = request.form.get("Q3") #Q3 refrigerated water 
        if answer3 == "yes":
            beach_box += 1

        answer4 = request.form.get("Q4") #Q4 Do you want multiple saunas on site
        if answer4 == "yes":
            beach_box += 1
        
        answer5 = request.form.get("Q5") #Q5 Other facilities onsite 
        if answer5 == "yes":
            luna += 1

        answer6 = request.form.get("Q6") #Q6 Sauna size 
        if answer6 == "6":
            beach_box += 1
        elif answer6 == "8":
            saunadelic +=1
        elif answer6 == "14":
            luna += 1
            beach_box +=1

        answer7 = request.form.get("Q7")#Q7 Sea view
        if answer7 == "yes":
            beach_box += 1
            luna += 1
        
        answer8 = request.form.get("Q8") #Q8 30 min booking slot
        if answer8 == "yes":
            luna += 1

        answer9 = request.form.get("Q9") #Q9 location
        if answer9 == "Hove":
            saunadelic +=1
        elif answer9 == "Kemptown":
            beach_box +=1
            luna +=1 # 'no preference' has no effect

        answer10 = request.form.get("Q10") #Q10 Book on the day
        if answer10 == "day":
            luna += 1         

        #Decide winner
        result = "TBC"
        result_1 = []
        dict = {}
        sauna_links_1 = []
        sauna_links = {"Saunadelic_link": "https://www.saunadelic.uk", #Put all links in dict and make blank where they are not a winner 
                       "Luna_Hut_link":   "https://www.lunahutsauna.co.uk/sealanes",
                       "BeachBox_link":   "https://beachboxspa.co.uk",
                       "Saunadelic": "Saunadelic",
                       "Beach_Box": "Beach Box",
                       "Luna_Hut": "Luna Hut",
                       }
        sauna_links_1.append(sauna_links)

        if luna == beach_box == saunadelic: # If all are tied 
            result = "Tie - you have scored every sauna equally!"   
            dict = {"Result": result}
            result_1.append(dict)
            print(result_1)

        elif luna == beach_box > saunadelic:
            result = "Tie - Luna Hut and Beach Box" #If Luna Hut and Beach Box tied
            dict = {"Result": result}
            result_1.append(dict)
            sauna_links["Saunadelic"] = ""

        elif luna == saunadelic > beach_box:
            result = "Tie - Luna Hut and Saunadelic" #If Luna and Saunadelic tied 
            dict = {"Result": result}
            result_1.append(dict)
            sauna_links["Beach_Box"] = ""

        elif saunadelic == beach_box > luna:
            result = "Tie - Beach Box and Saunadelic" #If BeachBox and Saunadelic tied 
            dict = {"Result": result}
            print(dict)
            result_1.append(dict)
            print(result_1)
            sauna_links["Luna_Hut"] = ""
        
        else:
            max_1 = max(luna, beach_box, saunadelic) #If a single winner, as identified using max
            if max_1 == luna: 
                result = "Luna Hut"
                sauna_links["Beach_Box"] = ""
                sauna_links["Saunadelic"] = ""

            elif max_1 == saunadelic:
                result = "Saunadelic"
                sauna_links["Beach_Box"] = ""
                sauna_links["Luna_Hut"] = ""
            else:
                result = "Beach Box"
                sauna_links["Saunadelic"] = ""
                sauna_links["Luna_Hut"] = ""
            print(f"Winner: {result}")
            dict = {"Result": result}
            result_1.append(dict)
        
        print(f"Saunadelic: {saunadelic}")
        print(f"BeachBox: {beach_box}")
        print(f"Luna Hut: {luna}")
        print(sauna_links["Saunadelic"])

        #Scrape Current temperature 
        temp = 0
        temp_list = []
        
        class Scraper:
             def __init__(self, site): 
                self.site = site 
            
             def scrape(self):
                r = urllib.request.urlopen(self.site) #Makes request to website and returns Response object with its HTML stored in it 
                html = r.read()
                parser = "html.parser"
                sp = BeautifulSoup(html, parser) #Parses html
                for tag in sp.find_all("div", attrs={"data-unit":"temperature"}): #Returns an iterable of all the tags it found - for each iteration of the loop, tag is assigned value of new tag object 
                    temp = (tag["data-c"])
                    temp_dict = {"Temperature": temp}
                    temp_list.append(temp_dict)
                    print(temp_dict)
                    break #Goes to the first line of loop only as this is the current temperature 
        sauna = "https://weather.metoffice.gov.uk/forecast/gcpchhy5p#?date=2025-04-11"
        Scraper(sauna).scrape()  
                
        return render_template("result.html", dict=result_1, sauna_links=sauna_links_1, temp_list=temp_list) 

    else:
        return render_template("quiz.html")

@app.route("/info")
def info(): 

    return render_template("info.html")

@app.route("/result")
def result():

    return render_template("result.html")



