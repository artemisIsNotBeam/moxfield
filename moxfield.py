from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re

urls=[
    "https://www.moxfield.com/decks/M5pyNPcta0OL9uJXraws0A",
    "https://www.moxfield.com/decks/OY2dWRkb6EqzQ-wSCWXnAw",
    "https://www.moxfield.com/decks/iQvbpRdsVkOrV7ITOov8fA",
    "https://www.moxfield.com/decks/ef5XQ00xJkKJAuQVihRMuA",
    "https://www.moxfield.com/decks/7VAB7wPq8kS352RZDvgRDQ",
    "https://www.moxfield.com/decks/gcliKlh4EEOl_l8lALwxSw",
    "https://www.moxfield.com/decks/vFibgbMBL0-qnIad6lyvcg",
    "https://www.moxfield.com/decks/CPWTHp_1IkWae3MtHfWg3Q",
    "https://www.moxfield.com/decks/ujpLJwzQWUimd5mNXm9Z2A",
    "https://www.moxfield.com/decks/lhGmLTD4CkKU31eI56bL3g",
    "https://www.moxfield.com/decks/u_grS8QbtkiViccdclf8cA",
    "https://www.moxfield.com/decks/6sKlRuY6_kycMS0_pYfH8w",
    "https://www.moxfield.com/decks/pxAR8PCf1kyZ_N89rFdsjw",
    "https://www.moxfield.com/decks/EJ_AdSj6gE6Tf092upBCcw",
    "https://www.moxfield.com/decks/EJ_AdSj6gE6Tf092upBCcw",
    "https://www.moxfield.com/decks/zozQJFLLfkibHX51uF4ijw",
    "https://www.moxfield.com/decks/sQVWnDu8f06gIYZNW_m7CQ",
    "https://www.moxfield.com/decks/ngnHw9feaUWPqTEXYKjihA",
    "https://www.moxfield.com/decks/Nb-MMLXEL0OX_M9ickYRfQ",
    "https://www.moxfield.com/decks/aLS0YcIPtUqrSdVSjxCmnQ",
    "https://www.moxfield.com/decks/IDcGz4pJLkKgpr-J8LcUvQ",
    "https://www.moxfield.com/decks/bnUxHxrJ80quGE_ttb5s2g",
    "https://www.moxfield.com/decks/pfCdqKOgyUSzK3EuGXUFgw",
    "https://www.moxfield.com/decks/rb-gKJcCDkOijaUd6v0Zhw",
    "https://www.moxfield.com/decks/2f2rYM0SZUCv9sfVoIC-ZQ",
    "https://www.moxfield.com/decks/CE9Yx8CiD0ugEccej3m98A",
    "https://www.moxfield.com/decks/8JBUheovykq6waJmBJ7iwQ",
    "https://www.moxfield.com/decks/rqPqo5qjRU6mIlcYsB5N_w",
    "https://www.moxfield.com/decks/MruH2lQoJkWE4XjJxQ4hFw",
    "https://www.moxfield.com/decks/LuZtnAgYRkyDhdGyd9Z_Qw"
]

formatConvert = {
    "Standard":1,
    "Modern":2,
    "Pioneer":3, 
    "Commander / EDH":4,
    "Legacy":5,
    "Vintage":5,
    "Pauper EDH":4,
    "Pauper":8,
}

def is_number(value):
  """Returns True if value is a number, False otherwise."""
  return isinstance(value, (int, float))


def search(url,browser):
        page = browser.new_page()
        page.goto(url)
        
        # Wait for the element with class "deckview" to appear
        page.wait_for_selector('.deckview')

        content = page.content()  # Gets the full HTML content after JS execution

        soup = BeautifulSoup(content, 'html.parser')

        name = soup.find_all('span', class_='deckheader-name')[0].text

        deckStats = soup.find_all('div', class_='d-flex text-muted mt-5 mx-auto')[0].find_all('strong')

        avgManaVal = float(deckStats[0].get_text())
        avgManaValNoLands=float(deckStats[1].get_text())
        totManaVal = int(deckStats[2].get_text())

        cardsInDeckString=soup.find_all('div',class_="text-nowrap d-inline-block me-2 me-sm-3")[0].get_text()
        
        cardsInDeck = int(re.split("\D+", cardsInDeckString)[0])

        Lands = int(cardsInDeck-(totManaVal/avgManaValNoLands))
        deckFormat = soup.find_all('a',class_="badge badge-header bg-primary py-1 px-2 fw-normal text-white text-caps me-2 cursor-pointer no-outline")[0].get_text()
        
        for key,value in formatConvert.items():
            if deckFormat == key:
                deckFormat = value

        if is_number(deckFormat)==False:
            print(link)
            print(deckFormat)
            raise ValueError("invalid type")
            
        
        return [
            cardsInDeck,    
            Lands,
            avgManaVal,
            totManaVal,
            deckFormat
        ]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)  # Launches a headless browser
    amount = 0
    with open("tesetData.csv", "a") as f:
        for link in urls:
            value=search(link,browser)
            amount+=1
            f.write(f"{value[0]},{value[1]},{value[2]},{value[3]},{value[4]}\n")
            print("doing thing "+str(amount))
    browser.close()
    print("finished!?")