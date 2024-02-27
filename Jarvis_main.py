import pyttsx3
import speech_recognition 
import sounddevice as sd
import numpy as np
from Dictapp import openappweb,closeappweb
from clap import Listen_for_claps
import os 
import pyautogui
import datetime
import mixer
import notification
import speedtest
from GreetMe import greetMe
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(
    api_key = os.environ.get("OPEN_AI_KEY"),
)

# def take_pass():
#     for i in range(3):
#         a = input("Enter Password to open Jarvis :- ")
#         pw_file = open("password.txt","r")
#         pw = pw_file.read()
#         pw_file.close()
#         if (a==pw):
#             print("WELCOME SIR ! PLZ SPEAK [WAKE UP] TO LOAD ME UP")
#             return 
#         elif (i==2 and a!=pw):
#             exit()

#         elif (a!=pw):
#             print("Try Again")

# from INTRO import play_gif
# play_gif


engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
rate = engine.setProperty("rate",250)


# def say(text):
#     enginer = pyttsx3.init("sapi5")
#     enginer.say(text)
#     enginer.runAndWait()
def speak(audio):
    engine.say(audio)
    engine.runAndWait()


chatStr = ""
def chat(query):
    if query=="none".lower():
        return 
    global chatStr
    chatStr += f"Atharva: {query}\n Jarvis: "
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": chatStr}],
        # prompt= chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo: Wrap this inside of a  try catch block
    speak(response.choices[0].message.content)
    chatStr += f"{response.choices[0].message.content}\n"
    print("gottin")
    print(response.choices[0].message.content)
    return response.choices[0].message.content



def alarm(query):
    timehere = open("Alarmtext.txt","a")
    timehere.write(query)
    timehere.close()
    os.startfile("alarm.py")


def takeCommand():
        r = speech_recognition.Recognizer()
        with speech_recognition.Microphone() as source:
            print("Listening.....")
            r.pause_threshold = 1
            r.energy_threshold = 300
            audio = r.listen(source,0,4)

        try:
            print("Understanding..")
            query  = r.recognize_google(audio,language='en-in')
            print(f"You Said: {query}\n")
            return query
        except Exception as e:
            print("Say that again")
            return "None"
    


threshold =65.0
Clap = False

def detect_clap(indata,frames,time,status):
    global Clap
    volume_norm = np.linalg.norm(indata)*10
    if volume_norm>threshold:
        print("Clapped!")
        Clap=True

def Listen_for_claps():
    print("Read for clap")
    with sd.InputStream(callback=detect_clap):
        print("clap detected")
        return sd.sleep(1000)
    

if __name__ == "__main__":
    print("in main")
    while True:
        Listen_for_claps()
        if Clap:
        # if "wake up".lower() in query:
        #     print("wake up in query")
            greetMe()
            # query = takeCommand().lower()
            # print("taken query")
            while True:
                query = takeCommand().lower()
                if "go to sleep" in query:
                    speak("Ok sir , You can call me anytime Just Clap and I'll be there for you")
                    Clap=False
                    break 
                # elif "change password" in query:
                #     speak("What's the new password")
                #     new_pw = input("Enter the new password\n")
                #     new_password = open("password.txt","w")
                #     new_password.write(new_pw)
                #     new_password.close()
                #     speak("Done sir")
                #     speak(f"Your new password is{new_pw}")
                elif "hello" in query:
                    speak("Hello sir, how are you ?")
                elif "i am fine" in query:
                    speak("that's great, sir")
                elif "how are you" in query:
                    speak("Perfect, sir")
                elif "thank you" in query:
                    speak("you are welcome, sir")
                elif "google" in query:
                    from SearchNow import searchGoogle
                    searchGoogle(query)
                elif "youtube" in query: 
                    from SearchNow import searchYoutube
                    searchYoutube(query)
                elif "wikipedia" in query:
                    from SearchNow import searchWikipedia
                    searchWikipedia(query)
                #  elif "temperature" in query:
                #     search = "temperature in delhi"
                #     url = f"https://www.google.com/search?q={search}"
                #     r  = requests.get(url)
                #     data = BeautifulSoup(r.text,"html.parser")
                #     temp = data.find("div", class_ = "BNeawe").text
                #     speak(f"current{search} is {temp}")
                # elif "weather" in query:
                #     search = "temperature in delhi"
                #     url = f"https://www.google.com/search?q={search}"
                #     r  = requests.get(url)
                #     data = BeautifulSoup(r.text,"html.parser")
                #     temp = data.find("div", class_ = "BNeawe").text
                #     speak(f"current{search} is {temp}")
                elif "the time" in query:
                    strTime = datetime.datetime.now().strftime("%H:%M")    
                    speak(f"Sir, the time is {strTime}")
                elif "finally sleep" in query:
                    speak("Going to sleep,sir")
                    exit()
                elif "open" in query:
                    openappweb(query)
                elif "close" in query:
                    closeappweb(query)
                elif "set an alarm" in query:
                    print("input time example:- 10 and 10 and 10")
                    speak("Set the time")
                    a = input("Please tell the time :- ")
                    alarm(a)
                    speak("Done,sir")
                elif "pause" in query:
                    pyautogui.press("k")
                    speak("video paused")
                elif "play" in query:
                    pyautogui.press("k")
                    speak("video played")
                elif "mute" in query:
                    pyautogui.press("m")
                    speak("video muted")
                elif "volume up" in query:
                    from keyboard import volumeup
                    speak("Turning volume up,sir")
                    volumeup()
                elif "volume down" in query:
                    from keyboard import volumedown
                    speak("Turning volume down, sir")
                    volumedown()
                elif "remember that" in query:
                    rememberMessage = query.replace("remember that","")
                    rememberMessage = query.replace("jarvis","")
                    speak("You told me to remember that"+rememberMessage)
                    remember = open("Remember.txt","a")
                    remember.write(rememberMessage)
                    remember.close()
                elif "what do you remember" in query:
                    remember = open("Remember.txt","r")
                    speak("You told me to remember that" + remember.read())
                # elif "tired" in query:
                #     speak("Playing your favourite songs, sir")
                #     a = (1,2,3) # You can choose any number of songs (I have only choosen 3)
                #     b = random.choice(a)
                #     if b==1:
                #     webbrowser.open()#Here put the link of your video)
                elif "news" in query:
                    from NewsRead import latestnews
                    latestnews()
                # elif "calculate" in query:
                #     from Calculatenumbers import WolfRamAlpha
                #     from Calculatenumbers import Calc
                #     query = query.replace("calculate","")
                #     query = query.replace("jarvis","")
                #     Calc(query)
                elif "whatsapp" in query:
                    from Whatsapp import sendMessage
                    sendMessage()
                elif "shutdown the system" in query:
                    speak("Are You sure you want to shutdown")
                    shutdown = input("Do you wish to shutdown your computer? (yes/no)")
                    if shutdown == "yes":
                        os.system("shutdown /s /t 1")

                    elif shutdown == "no":
                        break
                elif "schedule my day" in query:
                    tasks = [] #Empty list 
                    speak("Do you want to clear old tasks (Plz speak YES or NO)")
                    query = takeCommand().lower()
                    if "yes" in query:
                        file = open("tasks.txt","w")
                        file.write(f"")
                        file.close()
                        no_tasks = int(input("Enter the no. of tasks :- "))
                        i = 0
                        for i in range(no_tasks):
                            tasks.append(input("Enter the task :- "))
                            file = open("tasks.txt","a")
                            file.write(f"{i}. {tasks[i]}\n")
                            file.close()
                    elif "no" in query:
                        i = 0
                        no_tasks = int(input("Enter the no. of tasks :- "))
                        for i in range(no_tasks):
                            tasks.append(input("Enter the task :- "))
                            file = open("tasks.txt","a")
                            file.write(f"{i}. {tasks[i]}\n")
                            file.close()
                elif "show my schedule" in query:
                    file = open("tasks.txt","r")
                    content = file.read()
                    file.close()
                    # mixer.init()
                    # mixer.music.load("notification.mp3")
                    # mixer.music.play()
                    notification.notify(
                        title = "My schedule :-",
                        message = content,
                        timeout = 15
                        )
                elif "open" in query:   #EASY METHOD
                    query = query.replace("open","")
                    query = query.replace("jarvis","")
                    pyautogui.press("super")
                    pyautogui.typewrite(query)
                    pyautogui.sleep(2)
                    pyautogui.press("enter")  
                elif "internet speed" in query:
                    wifi  = speedtest.Speedtest()
                    upload_net = wifi.upload()/1048576         #Megabyte = 1024*1024 Bytes
                    download_net = wifi.download()/1048576
                    print("Wifi Upload Speed is", upload_net)
                    print("Wifi download speed is ",download_net)
                    speak(f"Wifi download speed is {download_net}")
                    speak(f"Wifi Upload speed is {upload_net}")

                elif "screenshot" in query:
                     import pyautogui #pip install pyautogui
                     im = pyautogui.screenshot()
                     im.save("ss.jpg")
                elif "click my photo" in query:
                    pyautogui.press("super")
                    pyautogui.typewrite("camera")
                    pyautogui.press("enter")
                    pyautogui.sleep(2)
                    speak("SMILE")
                    pyautogui.sleep(2)
                    pyautogui.press("enter")
                elif "focus mode" in query:
                    a = int(input("Are you sure that you want to enter focus mode :- [1 for YES / 2 for NO "))
                    if (a==1):
                        speak("Entering the focus mode....")
                        os.startfile(r"E:\python\GenAI\WiseWhisper\FocusMode.py")
                        exit()

                    
                    else:
                        pass
                elif "show my focus" in query:
                    from FocusGraph import focus_graph
                    focus_graph()
                # elif "translate" in query:
                #     from Translator import translategl
                #     query = query.replace("jarvis","")
                #     query = query.replace("translate","")
                #     translategl(query)
                # elif "ipl score" in query:
                #     from plyer import notification  #pip install plyer
                #     import requests #pip install requests
                #     from bs4 import BeautifulSoup #pip install bs4
                #     url = "https://www.cricbuzz.com/"
                #     page = requests.get(url)
                #     soup = BeautifulSoup(page.text,"html.parser")
                #     team1 = soup.find_all(class_ = "cb-ovr-flo cb-hmscg-tm-nm")[0].get_text()
                #     team2 = soup.find_all(class_ = "cb-ovr-flo cb-hmscg-tm-nm")[1].get_text()
                #     team1_score = soup.find_all(class_ = "cb-ovr-flo")[8].get_text()
                #     team2_score = soup.find_all(class_ = "cb-ovr-flo")[10].get_text()

                #     a = print(f"{team1} : {team1_score}")
                #     b = print(f"{team2} : {team2_score}")

                #     notification.notify(
                #         title = "IPL SCORE :- ",
                #         message = f"{team1} : {team1_score}\n {team2} : {team2_score}",
                #         timeout = 15
                #     )
                else:
                    chat(query)