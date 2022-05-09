import requests
import re
import urllib3
from bs4 import BeautifulSoup

#get vechicle data from user
print("Podaj rok produkcji samochodu:")
production_year = input()
print("Podaj VIN samochodu:")
vin_number = input()
print("Podaj numer rejestracyjny samochodu:")
reg_plate = input()

#this part is to fix ssl errors on website
requests.packages.urllib3.disable_warnings()
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
try:
    requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
except AttributeError:
    pass

#basic headers
headers = {
"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:99.0) Gecko/20100101 Firefox/99.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "pl,en-US;q=0.7,en;q=0.3",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Sec-GPC": "1",
        "Cache-Control": "max-age=0"}
#starting session
with requests.Session() as s:
    r = s.get("http://historiapojazdu.gov.pl/strona-glowna", headers=headers, verify=False)
    #getting p_auth key from website body
    m = re.search('p_auth=(.+?)"', r.text)
    if m:
       auth_key = m.group(1)
       soup = BeautifulSoup(r.text, "html.parser")
       if soup:
           #getting ViewState value from website body
           viewstate = soup.select('#_historiapojazduportlet_WAR_historiapojazduportlet_\:formularz > input:nth-child(7)')           
           viewstate = viewstate[0]['value']

           #setting headers
           headers = {
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:99.0) Gecko/20100101 Firefox/99.0",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                    "Accept-Language": "pl,en-US;q=0.7,en;q=0.3",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Upgrade-Insecure-Requests": "1",
                    "Sec-Fetch-Dest": "document",
                    "Sec-Fetch-Mode": "navigate",
                    "Sec-Fetch-Site": "same-origin",
                    "Sec-Fetch-User": "?1",
                    "Sec-GPC": "1"}
           #brute-forcing full registration date
           for month in range(1,13):
               for day in range(1,32):
                   registration_date=f"{day}.{month}.{production_year}"
            
           
                   payload={
                "_historiapojazduportlet_WAR_historiapojazduportlet_:formularz": "_historiapojazduportlet_WAR_historiapojazduportlet_:formularz",
                "javax.faces.encodedURL": "https://historiapojazdu.gov.pl/strona-glowna?p_p_id=historiapojazduportlet_WAR_historiapojazduportlet&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_cacheability=cacheLevelPage&p_p_col_id=column-1&p_p_col_count=1&_historiapojazduportlet_WAR_historiapojazduportlet__jsfBridgeAjax=true&_historiapojazduportlet_WAR_historiapojazduportlet__facesViewIdResource=%2Fviews%2Findex.xhtml",
                "_historiapojazduportlet_WAR_historiapojazduportlet_:rej": f"{reg_plate}",
                "_historiapojazduportlet_WAR_historiapojazduportlet_:vin": f"{vin_number}",
                "_historiapojazduportlet_WAR_historiapojazduportlet_:data": f"{registration_date}",
                "_historiapojazduportlet_WAR_historiapojazduportlet_:btnSprawdz": "Sprawdź+pojazd+»",
                "javax.faces.ViewState": f"{viewstate}"}
                   print (f"Checking date: {day}.{month}.{production_year}", end='\r', flush=True)
                   r = s.post(f"https://historiapojazdu.gov.pl/strona-glowna/-/hipo/historiaPojazdu/cepik?p_auth={auth_key}", headers=headers, verify=False, data=payload)
                   if ("Polisa" in r.text):
                       print(f"Data pierwszej rejestracji to: {registration_date}")
                       break
                   #time.sleep(0.3)
               else:
                   #time.sleep(0.3)
                   continue
               break
