import requests
import re
import os
from twilio.rest import Client
import datetime
from  time import sleep

# we can use environment variables to get our credentials safely, but
# I wanted to show some regex x)
def credentails():
    with open("credentials.txt", 'r') as f:
        lines = f.readlines()

    AUTH_TOKEN = re.search('[".-]+[.\w.-]+', lines[0]).group()[1:]
    SID = re.search('[".-]+[.\w.-]+', lines[1]).group()[1:]
    API_KEY = re.search('[".-]+[.\w.-]+', lines[2]).group()[1:]

    return AUTH_TOKEN, SID, API_KEY

AUTH_TOKEN, SID, API_KEY = credentails()

AUTH_TOKEN2 = "532aa770e714ac52ba1b181e2a9f7730"
SID2 = "AC54158ffd6431e8efa5c7c0d6b27bb5ac"
API_KEY2 = "b8a00843fab80db545bc18758bd1ddfb"

if((AUTH_TOKEN == AUTH_TOKEN2) and (SID == SID2) and (API_KEY2 == API_KEY)):
    print("Correct")
else: print("False")

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



while (True):
    # will check the time continuously until it's 6-am
    # then it'll send the weather report and sleep for 24 hours(at the end) making our code efficient
    now = datetime.datetime.now().strftime("%H")
    print(now)
    # if time is 6-am then we will send the message
    if now == "07":
        print("time correct")
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
        # we are getting wrong decription, debugging..
        ## description = response.json()["daily"][0]["weather"][0]["description"]

        if willRain:
            text = f"Don't forget to carry an umbrella :)"# \nToday's Description {description}.\n(this is 12 hour prediction from hour : {now})"
        else:
             text = f"It probably won't rain today :)"# \nToday's Description {description}.\n(this is 12 hour prediction from hour : {now})"

        client = Client(SID, AUTH_TOKEN)
        print("sending")

        print(text)
        for i in toNum:
            message = client.messages.create(
                to=i,
                from_=fromNum,
                body= text
                )
        print("done")
        # sleeps for 24 hours from 6-am so that our code will run only when it's 6-am
        sleep(86400)