import re

frequencies = ['FRQ', 'OCNL', 'CONS']
directions = ['N','NE','E','SE','S','SW','W','NW','UNKN']

metar = "KLIT 231847Z 15008KT 10SM -TSRA FEW015 BKN030CB OVC100 26/23 A3004 RMK AO2 RAE14B46 TSB05E27B46 OCNL LTGICCC DSNT W-N CB DSNT W-N P0000"


lightningDSNT = re.findall(r"\b(\w+\s)(LTG\w+\s)(\w+\s)(\S+\s)(\w+\s)(\w+\s)(\S+)\b", metar)
lightningOHD = re.findall(r"\b(\w+\s)(LTG\w+\s)(\w+\s)(\w+\s)(\w+\s)(\w+\s)(\S+)\b", metar)
lightningVC = re.findall(r"\b(\w+\s)(LTG\w+\s)(\w+\s)(\S+\s)(\w+\s)(\w+\s)(\S+\s)(\w+\s)(\S+)\b", metar)

print(lightningDSNT)
print(lightningOHD)
print(lightningVC)

#DSNT lighting[0] length should be 7
if(len(lightningDSNT) > 0):
    if lightningDSNT[0][2].strip() == 'DSNT':
        for frequency in frequencies:
            if frequency == lightningDSNT[0][0].strip():
                print("frequency okay")
        for direction in directions:
            if direction in lightningDSNT[0][3].strip():
                print("first direction okay")
            if direction in lightningDSNT[0][6].strip():
                print("second direction okay")
        if lightningDSNT[0][4].strip() == 'CB':
            print("CB position okay")
        if lightningDSNT[0][5].strip() == 'DSNT':
            print("second DSNT position okay")

#OHD lighting[0] length should be 7
if(len(lightningOHD) > 0):
    if lightningOHD[0][2].strip() == 'OHD':
        for frequency in frequencies:
            if frequency == lightningOHD[0][0].strip():
                print("frequency okay")
        for direction in directions:
            if direction in lightningOHD[0][6].strip():
                print("direction okay")
        if lightningOHD[0][3].strip() == 'TS':
            print("TS position okay")
        if lightningOHD[0][4].strip() == 'OHD':
            print("second OHD position okay")
        if lightningOHD[0][5].strip() == 'MOV':
            print("MOV position okay")


#VC lightning[0] should be length 9
if(len(lightningVC) > 0):
    if lightningVC[0][2].strip() == 'VC': #strip whitespace after VC
        for frequency in frequencies:
            if frequency == lightningVC[0][0].strip():
                print("frequency okay")
                
        for direction in directions:
            if direction in lightningVC[0][3].strip():
                print("first direction okay")
            if direction in lightningVC[0][6].strip():
                print("second direction okay")
            if direction in lightningVC[0][8].strip():
                print("third direction okay")
            
        if lightningVC[0][4].strip() == 'TS':
            print("TS position okay")

        if lightningVC[0][5].strip() == 'VC':
            print("VC position okay")

        if lightningVC[0][7].strip() == 'MOV':
            print("MOV position okay")

