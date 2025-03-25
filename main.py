import datetime
import os
import subprocess
import webbrowser
import time

import pyttsx3
import speech_recognition as sr
import wikipedia

NAME = "prashanthi"
print("initializing jarvis")
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good morning " + NAME)
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon " + NAME)
    else:
        speak("Good Evening " + NAME)
    speak("I am Jarvis. How may I help you?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 0.7
        audio = r.listen(source)
        try:
            print("Recognizing...")
            Query = r.recognize_google(audio, language='en-in')
            print("User said:", Query)
        except Exception as e:
            print(e)
            print("Please say that again.")
            return "None"
        return Query

def openApplication(app_name):
    if app_name == "notepad":
        subprocess.Popen("notepad.exe")
    elif app_name == "calculator":
        subprocess.Popen("calc.exe")
    else:
        speak("Application not found.")

def setCountdown(duration):
    speak(f"Starting a countdown for {duration}.")
    time_units = duration.split()
    total_seconds = 0

    for i in range(0, len(time_units), 2):
        value = int(time_units[i])
        unit = time_units[i + 1].lower()
        if "hour" in unit:
            total_seconds += value * 3600
        elif "minute" in unit:
            total_seconds += value * 60
        elif "second" in unit:
            total_seconds += value

    while total_seconds:
        mins, secs = divmod(total_seconds, 60)
        hours, mins = divmod(mins, 60)
        timer = '{:02d}:{:02d}:{:02d}'.format(hours, mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        total_seconds -= 1
    speak("Time's up!")

speak("Initializing Jarvis...")
wishMe()

while True:
    query = takeCommand().lower()
    if "open spotify" in query:
        speak("Opening Spotify")
        webbrowser.open("https://www.spotify.com")
        continue

    elif "open google" in query:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "open youtube" in query:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif "open wikipedia" in query:
        speak("Opening Wikipedia")
        webbrowser.open("https://www.wikipedia.org")

    elif "open" in query:
        app_name = query.split("open")[-1].strip()
        openApplication(app_name)

    elif "from wikipedia" in query:
        speak("Checking Wikipedia")
        query = query.replace("wikipedia", "")
        result = wikipedia.summary(query, sentences=4)
        speak("According to Wikipedia")
        speak(result)

    elif "what is your name" in query:
        speak("I am Jarvis, your desktop assistant.")

    elif "the time" in query:
        strtime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"{NAME}, the time is {strtime}")

    elif "set timer for" in query:
        try:
            duration = query.split("set timer for")[-1].strip()
            setCountdown(duration)
        except ValueError:
            speak("Sorry, I didn't understand the time duration.")

    elif "bye" in query:
        speak("Bye. Have a great day!")
        break