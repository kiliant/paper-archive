# Copyright (C) 2018 Thomas A. Kilian <kiliant@in.tum.de>. All Rights Reserved.

from selenium.webdriver import Firefox, FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import re
import sqlite3
import dateparser
import time
import os

DB_FILE = "/data/db.sqlite"
TARGET_DIR = "/data/"

def register_issue(db, issue, date, foreignID):
    cursor = db.cursor()
    cursor.execute("INSERT INTO issues(type, issue_date, foreignID) VALUES (?,?,?)", (issue, date.strftime('%Y-%m-%d'), foreignID))
    db.commit()
    return

# check whether we have to download issue
def lookup_issue(db, issue, date, foreignID):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM issues WHERE type=? AND issue_date=? AND foreignID=?", (issue, date.strftime('%Y-%m-%d'), foreignID))
    return cursor.fetchone() == None

def initiate_download(href):
    browser.get(href)

    button = WebDriverWait(browser, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".navigation-bar > div:nth-child(3) > sz-daily-download-thumb-tray-control:nth-child(2) > div:nth-child(1) > a:nth-child(1)"))
            )
    #button = browser.find_element_by_css_selector(".navigation-bar > div:nth-child(3) > sz-daily-download-thumb-tray-control:nth-child(2) > div:nth-child(1) > a:nth-child(1)")
    button.click()

    issue = browser.find_elements_by_css_selector(".navigation-bar > div:nth-child(2) > h1:nth-child(1)")[0].text
    date = dateparser.parse(browser.find_elements_by_css_selector(".navigation-bar > div:nth-child(2) > span:nth-child(2)")[0].text, languages=['de', 'en'], settings={'TIMEZONE': 'UTC'})

    m = re.search("webreader/(.*)", href)
    foreignID = m.group(1)
    if lookup_issue(db, issue, date, foreignID):
        print("issue ("+issue+", "+date.strftime('%Y-%m-%d')+", "+foreignID+") is fresh!")
        register_issue(db, issue, date, foreignID)
    else:
        print("issue ("+issue+", "+date.strftime('%Y-%m-%d')+", "+foreignID+") is already known")
        return

    download_whole = WebDriverWait(browser, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "span.thumbtray-download-options > a:nth-child(1)"))
            )

    #download_whole = browser.find_element_by_css_selector("span.thumbtray-download-options > a:nth-child(1)")
    download_whole.click()


if not os.path.isfile(DB_FILE):
    db = sqlite3.connect(DB_FILE)
    with open("schema.sql", "r") as f:
        db.cursor().executescript(f.read())
    db.commit()
else:
    db = sqlite3.connect(DB_FILE)

opts = Options()
opts.set_headless()
#opts.set_preference("browser.download.useDownloadDir", True);
opts.set_preference("browser.download.folderList", 2);
opts.set_preference("browser.download.manager.showWhenStarting", False);
opts.set_preference("browser.download.dir", TARGET_DIR);
opts.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf, application/octet-stream");
opts.set_preference("pdfjs.disabled", True)
browser = Firefox(firefox_options=opts)

browser.get('https://epaper.sueddeutsche.de/Stadtausgabe')

button = browser.find_element_by_link_text("Anmelden")
button.click()

username = browser.find_element_by_id("id_login")
password = browser.find_element_by_id("id_password")

username.send_keys(os.environ['SZ_USER'])
password.send_keys(os.environ['SZ_PASSWORD'])
browser.find_element_by_id("authentication-button").click()

elements = browser.find_elements_by_css_selector("div.day a")

links = []

for element in list(set(elements)):
    links.append(element.get_attribute("href"))

links = list(set(links))

for x in links:
    if x is not None:
        initiate_download(x)

while [f for f in os.listdir(TARGET_DIR) if os.path.isfile(os.path.join(TARGET_DIR, f)) and ".part" in f] != []:
    print("waiting for downloads to finish")
    time.sleep(5)

print("finished. terminating")

db.close()
browser.close()

