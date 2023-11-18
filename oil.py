from selenium import webdriver
from selenium.webdriver.common.by import By
import paho.mqtt.publish as publish
import json
import os
import time

user_name = os.environ['app_username']
password = os.environ['app_password']
mqtt_server =  os.environ['mqtt_server']
mqtt_user = os.environ['mqtt_user']
mqtt_password = os.environ['mqtt_password']

option = webdriver.ChromeOptions()

option.add_argument("--disable-gpu")
option.add_argument("--disable-extensions")
option.add_argument("--disable-infobars")
option.add_argument("--start-maximized")
option.add_argument("--disable-notifications")
option.add_argument('--headless')
option.add_argument('--no-sandbox')
option.add_argument('--disable-dev-shm-usage')

while True:
    browser = webdriver.Chrome(options=option)
    browser.set_window_size(1440, 900)
    browser.get("https://app.smartoilgauge.com/app.php")
    browser.find_element("id","inputUsername").send_keys(user_name)
    browser.find_element("id","inputPassword").send_keys(password)
    browser.find_element(By.CSS_SELECTOR,"button.btn").click()
    browser.implicitly_wait(3)

    var = browser.find_element(By.XPATH,'//p[contains(text(), "/")]').text
    fill_level = browser.find_element(By.XPATH,"//div[@class='ts_col ts_level']//div[@class='ts_col_val']//p").get_attribute("innerHTML")
    fill_level = fill_level.split(r"/")
    current_fill_level = fill_level[0]
    current_fill_proportion = round((float(str(fill_level[0])) / float(str(fill_level[1]))) * 100, 1)
    battery_status = browser.find_element(By.XPATH,"//div[@class='ts_col ts_battery']//div[@class='ts_col_val']//p").get_attribute("innerHTML")
    days_to_low = browser.find_element(By.XPATH,"//div[@class='ts_col ts_days_to_low']//div[@class='ts_col_val']//p").get_attribute("innerHTML")

    print('Current Fill Level: ' + str(current_fill_level) + 'gal')
    print('Current Fill Percentage: ' + str(current_fill_proportion) + '%')
    print('Battery Status: ' + str(battery_status))
    print('Days till 1/4 tank: ' + str(days_to_low))

    msgs = [{"topic": "oilgauge/tanklevel", "retain": True , "payload": json.dumps({"current_fill_level": current_fill_level,
                                                                "current_fill_proportion": current_fill_proportion,
                                                                "battery_status": battery_status,
                                                                "days_to_low": days_to_low }) }]
    browser.quit()
    publish.multiple(msgs, hostname=mqtt_server, port=1883, auth={'username':mqtt_user, 'password':mqtt_password})
    time.sleep(3600)