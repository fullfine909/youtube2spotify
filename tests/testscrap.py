from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions() 
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
#options.add_argument('--headless')

browser = webdriver.Chrome(executable_path="./drivers/chromedriver",options=options)
url = "https://www.youtube.com/watch?v=30M4fYGzfD8&feature=youtu.be&ab_channel=BE-AT.TV"
browser.get(url)

# first button
xp1 = '//*[@id="dismiss-button"]'
WebDriverWait(browser,2).until(EC.element_to_be_clickable((By.XPATH, xp1))).click()
#browser.find_element_by_xpath(xp1).click()

# second button
browser.switch_to.frame("iframe")
xp2 = '//*[@id="introAgreeButton"]/span/span'
WebDriverWait(browser,2).until(EC.element_to_be_clickable((By.XPATH, xp2))).click()
browser.switch_to.default_content()

# third button
xp3 = '//*[@id="more"]/yt-formatted-string'
WebDriverWait(browser,2).until(EC.element_to_be_clickable((By.XPATH, xp3))).click()

# MUSIC INFO
xp4 = '//*[@id="collapsible"]'
res = browser.find_element_by_xpath(xp4).text.split('\n')

browser.close()

idx = [int(i) for i,x in enumerate(res) if x =='Canción']

songs = []
for i in idx:
    s = {
        'name':res[i+1],
        'artist':res[i+3]
    }
    songs.append(s)

