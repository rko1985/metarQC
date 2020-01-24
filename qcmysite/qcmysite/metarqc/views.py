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
            URL = "https://aviationweather.gov/metar/data?ids=" + str(site) + "&format=raw&date=&hours=36"
            r = requests.get(URL)
            soup = BeautifulSoup(r.content, 'html.parser') 
            metars = soup.findAll('code')

            errors = []
            for metar in metars:

                metarsplit = ['','']

                if("RMK" in metar.text):
                    metarsplit = metar.text.split("RMK") #splitting before and after remarks
                    metarsplit[0] = " ".join(metarsplit[0].split()[1:]) #getting rid of station ID
                    
                if "RMK" not in metar.text: #if there is no RMK in metar
                    metarsplit[0] = metar.text
                    metarsplit[1] = ''
                
                ##WARNINGS
                if "CLR" in metar.text:        
                    errors.append("Warning, CLR in metar " + metar.text)
                    
                if "TS" in metarsplit[0]:
                    errors.append("Warning, TS in metar, check further manually " + metar.text)

                ##ERRORS        
                if "AUTO" in metar.text:        
                    errors.append("ERROR AUTO in metar " + metar.text)
                
                if("RA" in metarsplit[0]):
                    if(len(metarsplit) > 1):
                        if("VCSH" in metarsplit[1]):
                            errors.append("ERROR RA and VCSH " + metar.text)
            
                #Checking if clouds > 5K have 500 ft increments
                clrs = re.findall(r"CLR", metar.text)
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
                            errors.append("cloud layer error above 10k" + metar.text)  

                for sct in scts:
                    if(int(sct) > 50 and int(sct) <= 100):
                        if int(sct) % 5 != 0:
                            errors.append("cloud layer error between 5K and 10K" + metar.text)
                    if(int(sct) > 100):
                        if int(sct) % 10 != 0:
                            errors.append("cloud layer error above 10k" + metar.text)


                for bkn in bkns:
                    if(int(bkn) > 50 and int(bkn) <= 100):
                        if int(bkn) % 5 != 0:
                            errors.append("cloud layer error between 5K and 10K" + metar.text)
                    if(int(bkn) > 100):
                        if int(bkn) % 10 != 0:
                            errors.append("cloud layer error above 10k" + metar.text)

                for ovc in ovcs:
                    if(int(ovc) > 50 and int(ovc) <= 100):
                        if int(ovc) % 5 != 0:
                            errors.append("cloud layer error between 5K and 10K" + metar.text)
                    if(int(ovc) > 100):
                        if int(ovc) % 10 != 0:
                            errors.append("cloud layer error above 10k" + metar.text)


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

                #Missiny sky condition
                if (len(clrs) == 0 and len(fews) == 0 and len(scts) == 0 and len(bkns) == 0 and len(ovcs) == 0):
                    errors.append("ERROR: missing sky condition " + metar.text)

                #TS in present wx but no CB
                if "TS" in metarsplit[0]:
                    if "CB" not in metarsplit[0]:
                        errors.append("ERROR: TS in present WX, no CB in cloud layer " + metar.text)


                #LTG formatting
                frequencies = ['FRQ', 'OCNL', 'CONS']
                directions = ['N','NE','E','SE','S','SW','W','NW','UNKN','ALQDS']
                ltg_errors = [0,0,0,0,0,0,0]
                            
                lightningDSNT = re.findall(r"\b(\w+\s)(LTG\w+\s)(\DSNT\s)(\S+\s(?:AND \w+\s)?)(\w+\s)(\w+\s)(\S+\s(?:AND \w+\s)?)\b", metarsplit[1])
                lightningOHD = re.findall(r"\b(\w+\s)(LTG\w+\s)(\OHD\s)(\w+\s)(\w+\s)(\w+\s)(\S+)\b", metarsplit[1])
                lightningVC = re.findall(r"\b(\w+\s)(LTG\w+\s)(\VC\s)(\S+\s(?:AND \w+\s)?)(\w+\s)(\w+\s)(\S+\s(?:AND \w+\s)?)(\w+\s)(\S+)\b", metarsplit[1])

                
                if "LTG" in metarsplit[1]:
                    #DSNT lighting[0] length should be 7
                    if(len(lightningDSNT) > 0):
                        if lightningDSNT[0][2].strip() == 'DSNT':
                            for frequency in frequencies:
                                if frequency == lightningDSNT[0][0].strip():                    
                                    ltg_errors[0] += 1
                            for direction in directions:
                                if direction in lightningDSNT[0][3].strip():                    
                                    ltg_errors[1] += 1
                                if direction in lightningDSNT[0][6].strip():                    
                                    ltg_errors[2] += 1
                            if lightningDSNT[0][4].strip() == 'CB':                
                                ltg_errors[3] += 1
                            if lightningDSNT[0][5].strip() == 'DSNT':                
                                ltg_errors[4] += 1
                        if ltg_errors[0] == 0 or ltg_errors[1] == 0 or ltg_errors[2] == 0 or ltg_errors[3] == 0 or ltg_errors[4] == 0:
                            errors.append("Error in LTG remark " + metar.text)
                            ltg_errors = [0,0,0,0,0,0,0]
                        if "TS" in metarsplit[0]:
                            errors.append("LTG DSNT, TS in present wx " + metar.text)
                        if "CB" in metarsplit[0]:
                            errors.append("LTG DSNT, CB in cloud layer " + metar.text)

                    #OHD lighting[0] length should be 7
                    if(len(lightningOHD) > 0):
                        if lightningOHD[0][2].strip() == 'OHD':
                            for frequency in frequencies:
                                if frequency == lightningOHD[0][0].strip():
                                    ltg_errors[0] += 1
                            for direction in directions:
                                if direction in lightningOHD[0][6].strip():
                                    ltg_errors[1] += 1
                            if lightningOHD[0][3].strip() == 'TS':
                                ltg_errors[2] += 1
                            if lightningOHD[0][4].strip() == 'OHD':
                                ltg_errors[3] += 1
                            if lightningOHD[0][5].strip() == 'MOV':
                                ltg_errors[4] += 1
                        if ltg_errors[0] == 0 or ltg_errors[1] == 0 or ltg_errors[2] == 0 or ltg_errors[3] == 0 or ltg_errors[4] == 0:
                            errors.append("Error in LTG remark " + metar.text)
                            ltg_errors = [0,0,0,0,0,0,0]
                        if "TS" not in metarsplit[0]:
                            errors.append("LTG OHD, TS not in present wx " + metar.text)
                        if "CB" not in metarsplit[0]:
                            errors.append("LTG OHD, CB not in cloud layer " + metar.text)

                    #VC lightning[0] should be length 9
                    if(len(lightningVC) > 0):
                        if lightningVC[0][2].strip() == 'VC': #strip whitespace after VC
                            for frequency in frequencies:
                                if frequency == lightningVC[0][0].strip():
                                    ltg_errors[0] += 1                    
                            for direction in directions:
                                if direction in lightningVC[0][3].strip():
                                    ltg_errors[1] += 1
                                if direction in lightningVC[0][6].strip():
                                    ltg_errors[2] += 1
                                if direction in lightningVC[0][8].strip():
                                    ltg_errors[3] += 1                
                            if lightningVC[0][4].strip() == 'TS':
                                ltg_errors[4] += 1
                            if lightningVC[0][5].strip() == 'VC':
                                ltg_errors[5] += 1
                            if lightningVC[0][7].strip() == 'MOV':
                                ltg_errors[6] += 1            
                        if ltg_errors[0] == 0 or ltg_errors[1] == 0 or ltg_errors[2] == 0 or ltg_errors[3] == 0 or ltg_errors[4] == 0 or ltg_errors[5] == 0 or ltg_errors[6] == 0:
                            errors.append("Error in LTG remark " + metar.text)                    
                            ltg_errors = [0,0,0,0,0,0,0]
                        if "TS" not in metarsplit[0]:
                            errors.append("LTG VC, TS not in present wx " + metar.text)
                        if "CB" not in metarsplit[0]:
                            errors.append("LTG VC, CB not in cloud layer " + metar.text)

                if "LTG" in metarsplit[1]:
                    if len(lightningDSNT) == 0 and len(lightningOHD) == 0 and len(lightningVC) == 0:
                        errors.append("Error in lightning remarks " + metar.text)
       
        errors.append('Check complete.')
    
    else:
        errors = []

    return render(request, 'metarqc/index.html', {'errors' : errors})