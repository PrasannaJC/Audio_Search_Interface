'''
This code is jointly developed by:
Prasanna Chandrasekar

'''
import pyttsx3
import speech_recognition as sr
from pywhatkit import search
import PySimpleGUI as sg

r = sr.Recognizer()


def SpeakText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

#create gui window
#sg.Window(title="Audio Interface", layout=[[]], margins=(500, 300)).read()

while 1:
    try:
        with sr.Microphone() as source1:


            r.adjust_for_ambient_noise(source1, duration=0.5)
            audio1 = r.listen(source1)
            awakeText = r.recognize_google(audio1)
            awakeText = awakeText.lower()

            # "assistant" check - user wants to search something
            if str(awakeText) == "assistant":
                print("Please say your command...")

                searchText = r.listen(source1)

                inputText = r.recognize_google(searchText)
                inputText = inputText.lower()

                print("Did you say: \"" + inputText + "\"")  # This line is here just so you can see what has been interpreted.

                if str(inputText) == "end program":
                    raise SystemExit()
                print("Respond with either 'YES' or 'NO")


                audio2 = r.listen(source1)
                inputVerify = r.recognize_google(audio2)
                inputVerify = inputVerify.lower()
                print(inputVerify)
                if str(inputVerify) == "yes":
                    SpeakText(inputText)
                    search(inputText)

    except sr.RequestError as e:
        print("Couldn't recognize results; {0}".format(e))
    except sr.UnknownValueError:
        # if the speech recognizer can't recognize something as speech, it gets caught here
        # print("Unknown error occurred")
        print("Sorry I didn't get that. Please say \"Assistant\" to search.")

