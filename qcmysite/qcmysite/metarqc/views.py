from django.shortcuts import render

import requests
from bs4 import BeautifulSoup
import re

# Create your views here.
def index(request):

    if request.method == 'POST':
        sites = request.POST['site']
        sites = sites.split(" ")

        for site in sites:
            URL = "https://aviationweather.gov/metar/data?ids=" + str(sites) + "&format=raw&date=&hours=36"
            r = requests.get(URL)
            soup = BeautifulSoup(r.content, 'html.parser') 
            metars = soup.findAll('code')

            errors = []
            for metar in metars:

                if("RMK" in metar.text):
                    metarsplit = metar.text.split("RMK")
            
                ##WARNINGS
                if "CLR" in metar.text:        
                    errors.append("Warning, CLR in metar " + metar.text)
                if "TS" in metar.text:
                    errors.append("Warning, TS in metar, check further manually " + metar.text)

                ##ERRORS        
                if "AUTO" in metar.text:        
                    errors.append("ERROR AUTO in metar " + metar.text)

                if("RA" in metarsplit[0]):
                    if(len(metarsplit) > 1):
                        if("VCSH" in metarsplit[1]):
                            errors.append("ERROR RA and VCSH " + metar.text)

            #Checking if clouds > 5K have 500 ft increments
                fews = re.findall(r"FEW(\d+)", metar.text)
                scts = re.findall(r"SCT(\d+)", metar.text)
                bkns = re.findall(r"BKN(\d+)", metar.text)
                ovcs = re.findall(r"OVC(\d+)", metar.text)

                for few in fews:
                    if(int(few) > 50 and int(few) <= 100):
                        if int(few) % 5 != 0:
                            errors.append("cloud layer error between 5K and 10K " + metar.text)
                    if(int(few) > 100):
                        if int(few) % 10 != 0:
                            errors.append("cloud layer error above 10k " + metar.text)  

                for sct in scts:
                    if(int(sct) > 50 and int(sct) <= 100):
                        if int(sct) % 5 != 0:
                            errors.append("cloud layer error between 5K and 10K" + metar.text)
                    if(int(sct) > 100):
                        if int(sct) % 10 != 0:
                            errors.append("cloud layer error above 10k " + metar.text)


                for bkn in bkns:
                    if(int(bkn) > 50 and int(bkn) <= 100):
                        if int(bkn) % 5 != 0:
                            errors.append("cloud layer error between 5K and 10K " + metar.text)
                    if(int(bkn) > 100):
                        if int(bkn) % 10 != 0:
                            errors.append("cloud layer error above 10k " + metar.text)

                for ovc in ovcs:
                    if(int(ovc) > 50 and int(ovc) <= 100):
                        if int(ovc) % 5 != 0:
                            errors.append("cloud layer error between 5K and 10K " + metar.text)
                    if(int(ovc) > 100):
                        if int(ovc) % 10 != 0:
                            errors.append("cloud layer error above 10k " + metar.text)


                #Missing wind
                if "KT" not in metarsplit[0]:            
                    errors.append("ERROR missing wind " + metar.text)

                #Missing vis
                if "SM" not in metarsplit[0]:
                    if len(re.findall(r"\b\d{4}\b", metarsplit[0])) == 0:
                        errors.append("ERROR: no vis " + metar.text)

                #Missing temp/dp
                if len(re.findall(r"\b[M]?\d{2}/[M]?\d{2}\b", metarsplit[0])) == 0:
                    errors.append("ERROR: missing temp/dp " + metar.text)

                #Missing altimeter
                if len(re.findall(r"\b[A]\d{4}\b", metarsplit[0])) == 0:
                    errors.append("ERROR: missing altimeter " + metar.text)
       
    
    else:
        errors = []

    return render(request, 'metarqc/index.html', {'errors' : errors})