import requests
from bs4 import BeautifulSoup
import re

sites = ['ALAB', 'KBHM', 'KDHN', 'KHSV', 'KMOB', 'KMGM', 'ALAS', 'PALH', 'PAMR', 'PANC', 'PANI', 'PABR', 'PABE', 'PACV', 'PASC', 'PADL', 'PAFA', 'PAGA', 'PAHO', 'PAJN', 'PAEN', 'PAKT', 'PAKN', 'PADQ', 'PAOT', 'PAOM', 'PAPG', 'PASI', 'PASM', 'PAUN', 'PADU', 'PAVD', 'PAWG', 'PAYA', 'ARIZ', 'KIFP', 'KFLG', 'KGCN', 'KIWA', 'KPGA', 'KPHX', 'KTUS', 'KNYL', 'MCAS', 'ARKA', 'KXNA', 'KFSM', 'KLIT', 'KTXK', 'CALI', 'KACV', 'KBFL', 'KBUR', 'KFAT', 'KLGB', 'KLAX', 'KMMH', 'KMRY', 'KOAK', 'KONT', 'KPSP', 'KRDD', 'KSMF', 'KSAN', 'KSFO', 'KSJC', 'KSBP', 'KSNA', 'KSBA', 'KSMX', 'KSTS', 'KSCK', 'COLO', 'KASE', 'KCOS', 'KDEN', 'KDRO', 'KEGE', 'KGJT', 'KGUC', 'KHDN', 'KMTJ', 'CONN', 'KBDL', 'KHVN', 'DELA', 'KILG', 'FLOR', 'KDAB', 'KFLL', 'KRSW', 'KGNV', 'KJAX', 'KEYW', 'KMLB', 'KMIA', 'KMCO', 'KSFB', 'KECP', 'KPNS', 'KPGD', 'KSRQ', 'KSGJ', 'KPIE', 'KTLH', 'KTPA', 'KVPS', 'KPBI', 'GEOR', 'KABY', 'KATL', 'KAGS', 'KBQK', 'KCSG', 'KSAV', 'KVLD', 'HAWA', 'PHTO', 'PHNL', 'PHOG', 'PHKO', 'PHMK', 'PHNY', 'PHLI', 'IDAH', 'KBOI', 'KSUN', 'KIDA', 'KLWS', 'KPIH', 'KTWF', 'ILLI', 'KBLV', 'KBMI', 'KCMI', 'KORD', 'KMDW', 'KMWA', 'KMLI', 'KPIA', 'KUIN', 'KRFD', 'KSPI', 'INDI', 'KEVV', 'KFWA', 'KIND', 'KSBN', 'IOWA', 'KCID', 'KDSM', 'KDBQ', 'KSUX', 'KALO', 'KANS', 'KGCK', 'KMHK', 'KFOE', 'KICT', 'KENT', 'KCVG', 'KLEX', 'KSDF', 'KOWB', 'KPAH', 'LOUI', 'KAEX', 'KBTR', 'KLFT', 'KLCH', 'KMLU', 'KMSY', 'KSHV', 'MAIN', 'KBGR', 'KPWM', 'KPQI', 'KRKD', 'MARY', 'KBWI', 'KHGR', 'KSBY', 'MASS', 'KBOS', 'KHYA', 'KACK', 'KPVC', 'KMVY', 'KORH', 'MICH', 'KAPN', 'KDTW', 'KESC', 'KFNT', 'KGRR', 'KCMX', 'KIMT', 'KAZO', 'KLAN', 'KSAW', 'KMKG', 'KPLN', 'KMBS', 'KCIU', 'KTVC', 'MINN', 'KBJI', 'KBRD', 'KDLH', 'KHIB', 'KINL', 'KMSP', 'KRST', 'KSTC', 'MISS', 'KGTR', 'KGPT', 'KJAN', 'MISS', 'KCOU', 'KJLN', 'KMCI', 'KSGF', 'KSTL', 'MONT', 'KBIL', 'KBZN', 'KBTM', 'KGTF', 'KHLN', 'KGPI', 'KMSO', 'KSDY', 'NEBR', 'KGRI', 'KLNK', 'KOMA', 'NEVA', 'KBVU', 'KEKO', 'KLAS', 'KVGT', 'KRNO', 'HAMP', 'KLEB', 'KMHT', 'KPSM', 'JERS', 'KACY', 'KTTN', 'KEWR', 'MEXI', 'KABQ', 'KHOB', 'KROW', 'KSAF', 'YORK', 'KALB', 'KBGM', 'KBUF', 'KELM', 'KFRG', 'KISP', 'KITH', 'KJFK', 'KLGA', 'KSWF', 'KIAG', 'KPBG', 'KROC', 'KSYR', 'KART', 'KHPN', 'NORT', 'KAVL', 'KCLT', 'KJQF', 'KFAY', 'KGSO', 'KPGV', 'KOAJ', 'KEWN', 'KRDU', 'KILM', 'NORT', 'KBIS', 'KDIK', 'KFAR', 'KGFK', 'KMOT', 'KISN', 'OHIO', 'KCAK', 'KLUK', 'KCLE', 'KCMH', 'KLCK', 'KDAY', 'KTOL', 'KYNG', 'OKLA', 'KLAW', 'KOKC', 'KTUL', 'OREG', 'KEUG', 'KMFR', 'KOTH', 'KPDX', 'KRDM', 'PENN', 'KABE', 'KERI', 'KMDT', 'KLBE', 'KPHL', 'KPIT', 'KUNV', 'KAVP', 'KIPT', 'RHOD', 'KBID', 'KPVD', 'KWST', 'SOUT', 'KCHS', 'KCAE', 'KFLO', 'KGSP', 'KHXD', 'KMYR', 'SOUT', 'KABR', 'KRAP', 'KFSD', 'TENN', 'KTRI', 'KCHA', 'KTYS', 'KMEM', 'KBNA', 'TEXA', 'KABI', 'KAMA', 'KAUS', 'KBPT', 'KBRO', 'KCLL', 'KCRP', 'KDAL', 'KDFW', 'KELP', 'KGRK', 'KHRL', 'KIAH', 'KHOU', 'KLRD', 'KGGG', 'KLBB', 'KMFE', 'KMAF', 'KSJT', 'KSAT', 'KTYR', 'KACT', 'KSPS', 'UTAH', 'KCDC', 'KOGD', 'KPVU', 'KSLC', 'KSGU', 'VERM', 'KBTV', 'VIRG', 'KCHO', 'KLYH', 'KPHF', 'KORF', 'KRIC', 'KROA', 'KDCA', 'KIAD', 'WASH', 'KBLI', 'KFHR', 'KPSC', 'KPUW', 'KBFI', 'KSEA', 'KGEG', 'KALW', 'KEAT', 'KYKM', 'WEST', 'KCKB', 'KCRW', 'KCKB', 'KHTS', 'KMGW', 'WISC', 'KATW', 'KEAU', 'KGRB', 'KLSE', 'KMSN', 'KMKE', 'KCWA', 'KRHI', 'WYOM', 'KCPR', 'KCOD', 'KGCC', 'KJAC', 'KLAR', 'KRKS', 'AMER', 'NSTU', 'GUAM', 'PGUM', 'NORT', 'PGSN', 'PGRO', 'PGWT', 'PUER', 'TJBQ', 'TJRV', 'TJCP', 'TJPS', 'TJSJ', 'TJIG', 'TJVQ', 'VIRG', 'TIST', 'TISX']
#sites = ['PHKO']

for site in sites:
    
    URL = "https://aviationweather.gov/metar/data?ids=" + site + "&format=raw&date=&hours=36"
    r = requests.get(URL) 

    soup = BeautifulSoup(r.content, 'html5lib') 
    metars = soup.findAll('code')

    for metar in metars:

        if("RMK" in metar.text):
            metarsplit = metar.text.split("RMK")
        
        ##WARNINGS
        '''if "CLR" in metar.text:        
            print("Warning, CLR in metar " + metar.text)
            
        if "TS" in metarsplit[0]:
            print("Warning, TS in metar, check further manually " + metar.text)

        ##ERRORS        
        if "AUTO" in metar.text:        
            print("ERROR AUTO in metar " + metar.text)'''
        
        if("RA" in metarsplit[0]):
            if(len(metarsplit) > 1):
                if("VCSH" in metarsplit[1]):
                    print("ERROR RA and VCSH " + metar.text)
       
        #Checking if clouds > 5K have 500 ft increments
        fews = re.findall(r"FEW(\d+)", metar.text)
        scts = re.findall(r"SCT(\d+)", metar.text)
        bkns = re.findall(r"BKN(\d+)", metar.text)
        ovcs = re.findall(r"OVC(\d+)", metar.text)

        for few in fews:
          if(int(few) > 50 and int(few) <= 100):
            if int(few) % 5 != 0:
              print("cloud layer error between 5K and 10K " + metar.text)
          if(int(few) > 100):
            if int(few) % 10 != 0:
              print("cloud layer error above 10k" + metar.text)  

        for sct in scts:
          if(int(sct) > 50 and int(sct) <= 100):
            if int(sct) % 5 != 0:
              print("cloud layer error between 5K and 10K" + metar.text)
          if(int(sct) > 100):
            if int(sct) % 10 != 0:
              print("cloud layer error above 10k" + metar.text)


        for bkn in bkns:
          if(int(bkn) > 50 and int(bkn) <= 100):
            if int(bkn) % 5 != 0:
              print("cloud layer error between 5K and 10K" + metar.text)
          if(int(bkn) > 100):
            if int(bkn) % 10 != 0:
              print("cloud layer error above 10k" + metar.text)

        for ovc in ovcs:
          if(int(ovc) > 50 and int(ovc) <= 100):
            if int(ovc) % 5 != 0:
              print("cloud layer error between 5K and 10K" + metar.text)
          if(int(ovc) > 100):
            if int(ovc) % 10 != 0:
              print("cloud layer error above 10k" + metar.text)


        #Missing wind
        if "KT" not in metarsplit[0]:            
            print("ERROR missing wind " + metar.text)

        #Missing vis
        if "SM" not in metarsplit[0]:
            if len(re.findall(r"\b\d{4}\b", metarsplit[0])) == 0:
                print("ERROR: no vis " + metar.text)

        #Missing temp/dp
        if len(re.findall(r"\b[M]?\d{2}/[M]?\d{2}\b", metarsplit[0])) == 0:
            print("ERROR: missing temp/dp " + metar.text)

        #Missing altimeter
        if len(re.findall(r"\b[A]\d{4}\b", metarsplit[0])) == 0:
            print("ERROR: missing altimeter " + metar.text)
    

