import requests
import re
import os
from twilio.rest import Client
import datetime
from  time import sleep


#our credentials
AUTH_TOKEN = os.environ.get('WEATHER_API_KEY')
API_KEY = os.environ.get('TWILIO_AUTH_TOKEN')
SID = "AC54158ffd6431e8efa5c7c0d6b27bb5ac"

# phone numbers where we are sending our report
toNum = ["+9779869422081", "+9779860459806"]

# phone number that'll send our message
fromNum = "+16196584465"

# get our twilio api token, sid, and open weather api key


# parameters that we use in our get request
parameters = {
    'lat': 27.7309,
    'lon': 85.2955,
    'exclude': 'current,minutely,alerts',
    'appid': API_KEY,
}



while (False):
    # will check the time continuously until it's 6-am
    # then it'll send the weather report and sleep for 24 hours(at the end) making our code efficient
    now = datetime.datetime.now().strftime("%H")

    # if time is 6-am then we will send the message
    if now == "6":

        response = requests.get(url= "https://api.openweathermap.org/data/2.5/onecall", params= parameters)

        willRain = False

        # loop over 12 hour of weather data
        for hour in response.json()["hourly"][:12]:

            # parse to get our weather id
            rain = hour['weather'][0]['id']

            # if our rain, i.e, any of next 12 hour of weather data is less than 700
            # it will rain, I don't know how we get that threshold but it is what it is
            if rain < 700:
                willRain = True
                break

        text = ""

        # parse the json to get today's description
        description = response.json()["daily"][0]["weather"][0]["description"]

        if willRain:
            text = f"Don't forget to carry an umbrella :)\nToday's Description = {description}.\n(this is 12 hour prediction from hour : {now})"
        else:
             text = f"It probably won't rain today :)\nToday's Description = {description}.\n(this is 12 hour prediction from hour : {now})"

        client = Client(SID, AUTH_TOKEN)

        for i in toNum:
            message = client.messages.create(
                to=i,
                from_=fromNum,
                body= text
                )
        # sleeps for 24 hours from 6-am so that our code will run only when it's 6-am
        sleep(86400)