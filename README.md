# Docker Scraper for Oil Guage

# Use
Set docker environment variables:
  app_username = Username to app.smartoilgauge.com
  app_password = Password to app.smartoilgauge.com
  mqtt_server = Where your mqtt server is
  mqtt_user = username to connect to your mqtt server
  mqtt_password = password to connect to your mqtt server

Start Docker Container

Container will scrape https://www.smartoilgauge.com/ hourly and send tank results to the MQTT Server specified. It is recommended to set your tank upload interval to hourly as the webpage only shows the latest interval, not past hourly values. This does drain the battery quicker, the company estimates it to be a yearly battery change with a 1hr upload interval.