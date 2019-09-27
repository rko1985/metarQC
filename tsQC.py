import re

metar = "KLIT 260053Z 16006KT 10SM SCT120 26/19 A2985 RMK AO2 SLP107 OCNL LTGIC DSNT NE-W AND W CB DSNT NE T02560189"

if("RMK" in metar):
    metarsplit = metar.split("RMK")

frequencies = ['FRQ', 'OCNL', 'CONS']
directions = ['N','NE','E','SE','S','SW','W','NW','UNKN','ALQDS']
ltg_errors = [0,0,0,0,0,0,0]
            
lightningDSNT = re.findall(r"\b(\w+\s)(LTG\w+\s)(\DSNT\s)(\S+\s(?:AND \w+\s)?)(\w+\s)(\w+\s)(\S+\s(?:AND \w+\s)?)\b", metarsplit[1])
lightningOHD = re.findall(r"\b(\w+\s)(LTG\w+\s)(\OHD\s)(\w+\s)(\w+\s)(\w+\s)(\S+)\b", metarsplit[1])
lightningVC = re.findall(r"\b(\w+\s)(LTG\w+\s)(\VC\s)(\S+\s(?:AND \w+\s)?)(\w+\s)(\w+\s)(\S+\s(?:AND \w+\s)?)(\w+\s)(\S+)\b", metarsplit[1])

print(lightningDSNT)
print(lightningOHD)
print(lightningVC)

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
            print("Error in LTG remark " + metar)
            print(ltg_errors)
            ltg_errors = [0,0,0,0,0,0,0]

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
            print("Error in LTG remark " + metar)
            print(ltg_errors)
            ltg_errors = [0,0,0,0,0,0,0]

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
            print("Error in LTG remark " + metar)
            print(ltg_errors)
            ltg_errors = [0,0,0,0,0,0,0]

if "LTG" in metarsplit[1]:
    if len(lightningDSNT) == 0 and len(lightningOHD) == 0 and len(lightningVC) == 0:
        print("Error in lightning remarks " + metar)
