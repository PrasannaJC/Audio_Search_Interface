# Utils file for methods to break down spech recognition
import speech_recognition as sr
from pywhatkit import search
import PySimpleGUI as sg
import pyttsx3
from threading import Thread
from time import sleep

r = sr.Recognizer()

def SpeakText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

def awakeThread(microphone, r):
    while True:
        try:
            with microphone as source1:
                r.adjust_for_ambient_noise(source1, duration=0.5)
                audio1 = r.listen(source1)
                awakeText = r.recognize_google(audio1)
                awakeText = awakeText.lower()
            if str(awakeText) == "assistant":
                return (awakeText)
        except sr.UnknownValueError:
            # if the speech recognizer can't recognize something as speech, it gets caught here
            print("Sorry I didn't get that. Please say \"Assistant\" to search. - awakeThread")

def listenForSearchThread(microphone, r):
    while True:
        try:
            with microphone as source1:
                r.adjust_for_ambient_noise(source1, duration=0.5)
                print("Please say your command...")
                searchText = r.listen(source1)
                inputText = r.recognize_google(searchText)
                inputText = inputText.lower()

                print("Did you say: \"" + inputText + "\"")
                #if inputText != None:
                return inputText
                break

        except sr.UnknownValueError:
            # if the speech recognizer can't recognize something as speech, it gets caught here
            print("Sorry I didn't get that. Please say \"Assistant\" to search. - listenForSearchThread")

def validationThread(microphone, r, searchText):
    success = "yes"
    fail = "no"
    end = "EXIT"
    while True:
        try:
            with microphone as source1:
                r.adjust_for_ambient_noise(source1, duration=0.5)
                audio2 = r.listen(source1)
                inputVerify = r.recognize_google(audio2)
                inputVerify = inputVerify.lower()
                if str(inputVerify) == "yes":
                    SpeakText(searchText)
                    search(searchText)
                    sleep(1)
                    return success
                    break
                if str(inputVerify) == "no":
                    #return fail
                    sleep(1)
                    return fail
                    break
                if str(inputVerify) == "end program":
                    sleep(1)
                    return end

        except sr.UnknownValueError:
            # if the speech recognizer can't recognize something as speech, it gets caught here
            print("Sorry I didn't get that. Please say \"Assistant\" to search. - validationThread")

def listenThread():
    while True:
        try:
            with sr.Microphone() as source1:
                r.adjust_for_ambient_noise(source1, duration=0.5)
                audio1 = r.listen(source1)
                awakeText = r.recognize_google(audio1)
                awakeText = awakeText.lower()

                print(awakeText)
                # "assistant" check - user wants to search something
                if str(awakeText) == "assistant":
                    return(awakeText)
                    print("Please say your command...")
                    searchText = r.listen(source1)

                    inputText = r.recognize_google(searchText)
                    inputText = inputText.lower()

                    print("Did you say: \"" + inputText + "\"")

                    if str(inputText) == "end program":
                        # raise SystemExit()
                        return "EXIT"
                    print("Respond with either 'YES' or 'NO")

                    audio2 = r.listen(source1)
                    inputVerify = r.recognize_google(audio2)
                    inputVerify = inputVerify.lower()
                    print(inputVerify)
                    if str(inputVerify) == "yes":
                        SpeakText(inputText)
                        search(inputText)
                        return inputText
        except sr.RequestError as e:
            print("Couldn't recognize results; {0}".format(e))
        except sr.UnknownValueError:
            # if the speech recognizer can't recognize something as speech, it gets caught here
            # print("Unknown error occurred")
            print("Sorry I didn't get that. Please say \"Assistant\" to search.")

