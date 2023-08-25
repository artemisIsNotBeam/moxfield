from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

#   python goldfishScrape.py

url='https://www.mtggoldfish.com/deck/5804980#paper'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)  # Launches a headless browser
    page = browser.new_page()
    page.goto(url)
    
    # You might want to add some delay or wait for a specific element to ensure the page loads fully.
    # For example:
    # page.wait_for_selector("some-css-selector")

    content = page.content()  # Gets the full HTML content after JS execution
    browser.close()

    soup = BeautifulSoup(content, 'html.parser')
    #text = soup.get_text(strip=True)
    text = soup.get_text()

    name = soup.find_all('h1', class_='title')[0].text
    print(name)

    '''
    decklist = soup.find_all('tbody')[0]
    spans = decklist.find_all('span')

    print(spans)
    ''' 
    print("deck list:")
    input_tag = soup.find(id='deck_input_deck')
    print(input_tag.get('value'))
