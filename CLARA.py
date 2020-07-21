import pyttsx3 # text to speech
import datetime # date and time 
import speech_recognition as sr #to get commands
import wikipedia # search function
import smtplib #SEND MAIL
import webbrowser as wb #SEARCH IN BROWSER
import os #SHUTDOWN PURPOSES
import pyautogui #SCREENSHOT UTILITY
import psutil # CPU DETAILS
import pyjokes #jokes :)
import requests,json #weather scrap

engine = pyttsx3.init()
voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
engine.setProperty('voice',voice_id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def time():
    T = datetime.datetime.now().strftime("%I:%M:%S")
    speak("The current time is")
    speak(T)
    
def date():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    day = int(datetime.datetime.now().day)
    speak("The current date is")
    speak(day)
    speak(month)
    speak(year)
    
def wisher():
    speak("Welcome Back Sir!")
    h = datetime.datetime.now().hour
    if h>=6 and h<12:
        speak("Good Morning Sir!")
    elif h>=12 and h<18:
        speak("Good Afternoon Sir!")
    elif h>=18 and h<24:
        speak("Good Evening Sir!")
    else:
        speak("Good Night Sir!")
    speak("CLARA at your service Sir how can i help you?")
    
#wisher()

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing....")
        query = r.recognize_google(audio, language='en-in')
        print(query)

    except Exception as e:
        print(e)
        speak("Say that again please .....")

        return "None"

    return query

#takecommand()

def weatherforecast(city):
    api_key = "0b3fe689bfbe4da4913510d0ee3799f8"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    city_name = city
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url) 
    x = response.json()
    if x["cod"] != "404": 
        y = x["main"]
        current_temperature = y["temp"]-273.15
        current_pressure = y["pressure"]
        current_humidiy = y["humidity"] 
        z = x["weather"] 
        weather_description = z[0]["description"] 
        speak("Current Temperature"+str(current_temperature))
        speak("Atmospheric Pressure"+str(current_pressure))    
        speak("humidity"+str(current_humidiy))
        speak("description"+str(weather_description)) 
    else: 
        speak(" City Not Found ")


def sendemail(to,content):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login("gmail_id","gmail_password")
    server.sendmail("gmail_id",to,content)
    server.close()

def screenshot():
    img = pyautogui.screenshot()
    img.save("screen.png")

def cpu():
    usage = str(psutil.cpu_percent())
    speak("Your CPU is at" + usage)
    battery = psutil.sensors_battery()
    speak("Battery is at")
    speak(battery.percent)

def jokes():
    speak(pyjokes.get_joke())


if __name__ == "__main__":
    wisher()
    while True:
        query =  takecommand().lower()

        if 'time' in query:
            time()

        elif 'date' in query:
            date()

        elif 'wikipedia' in query:
            speak("Searching On wikipedia Sir....!")
            query = query.replace("wikipedia","")
            result = wikipedia.summary(query,sentences=2)
            print(result)
            speak(result)

        elif 'send a mail' in query:
            try:
                speak("What should i write in mail sir?...")
                content = takecommand()
                speak("Enter The mail address of reciever...")
                #to = takecommand()
                to = input("Email:")
                sendemail(to,content)
                speak("Email Succesfully sent sir!...")
            except Exception as e:
                print(e)
                speak("Unable to send the mail sir...")

        elif 'search' in query:
            speak("What should i search for you sir...")
            chromepath = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
            search = takecommand().lower()
            wb.get(chromepath).open_new_tab(search+'.com')

        elif 'logout' in query:
            os.system("Shutdown -1")

        elif 'shutdown' in query:
            os.system("Shutdown /s /t 1")

        elif 'restart' in query:
            os.system("Shutdown /r /t 1")

        elif 'play music' in query:
            songs_dir = 'Enter Your Music Directory :D'
            songs = os.listdir(songs_dir)
            os.startfile(os.path.join(songs_dir,songs[1]))

        elif 'remember that' in query:
            speak("what should i remember for you sir....")
            data = takecommand()
            speak("you asked me to remember that"+data)
            remember = open('data.txt','w')
            remember.write(data)
            remember.close()

        elif 'did i told you something' in query:
            remember = open('data.txt', 'r')
            speak("You asked me to remember that" + remember.read())

        elif 'screenshot' in query:
            speak("Taking a screenshot for you sir...")
            screenshot()
            speak("screenshot saved successfully sir...")

        elif 'cpu' in query:
            cpu()

        elif 'joke' in query:
            speak("Finding a good joke for you")
            jokes()
        
        elif 'weather' in query:
            speak("which city's weather you want to know Sir ....")
            city = takecommand().lower()
            weatherforecast(city)
        
        elif 'offline' in query:
            speak("Going Offline Sir Have a great day")
            quit()