'''
This code is jointly developed by:
Prasanna Chandrasekar


'''
import gtts
import pyttsx3
import speech_recognition as sr
#import pyttsx3
from playsound import playsound
from pywhatkit import search

r = sr.Recognizer()

def SpeakText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

while(1):
    try:
        with sr.Microphone() as source1:

            r.adjust_for_ambient_noise(source1, duration=0.5)
            audio1 = r.listen(source1)

            inputText = r.recognize_google(audio1)
            inputText = inputText.lower()

            print("Did you say " + inputText)
            SpeakText(inputText)
            search(inputText)
    except sr.RequestError as e:
        print("Couldn't recognize results; {0}".format(e))
    except sr.UnknownValueError:
        print("Unknown error occurred")


'''
tts = gtts.gTTS("what's up lads!")
not needed
tts.save("hello2.mp3")
playsound("hello2.mp3")
'''