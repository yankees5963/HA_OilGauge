from selenium import webdriver
from selenium.webdriver.common.by import By
import paho.mqtt.publish as publish
import json
from selenium.webdriver.chrome.service import Service

mqtt_server =  "localhost"
mqtt_user = "oil"
mqtt_password = "mcNajqD8GZiDP2"

option = webdriver.ChromeOptions()

option.add_argument("--disable-gpu")
option.add_argument("--disable-extensions")
option.add_argument("--disable-infobars")
option.add_argument("--start-maximized")
option.add_argument("--disable-notifications")
option.add_argument('--headless')
option.add_argument('--no-sandbox')
option.add_argument('--disable-dev-shm-usage')

service_obj = Service("/usr/bin/chromedriver")
browser = webdriver.Chrome(service=service_obj, options=option)
browser.set_window_size(1440, 900)
browser.get("https://www.alliancefuel.com/")

price75 = browser.find_element(By.XPATH,"//*[contains(text(), '75 - 99 gallons:')]").text.split("$",1)[1]
price100 = browser.find_element(By.XPATH,"//*[contains(text(), '100 - 149 gallons:')]").text.split("$",1)[1]
price150 = browser.find_element(By.XPATH,"//*[contains(text(), '150+ gallons:')]").text.split("$",1)[1]

print(price75)
print(price100)
print(price150)

browser.quit()

msgs = [{"topic": "oil/pricelist", "retain": True , "payload": json.dumps({"Oil_75_99": price75,
                                                            "Oil_100_149": price100,
                                                            "Oil_150": price150 }) }]
browser.quit()
publish.multiple(msgs, hostname=mqtt_server, port=1883, auth={'username':mqtt_user, 'password':mqtt_password})