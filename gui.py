# file for managing gui settings

import PySimpleGUI as sg
import speech_recognition as sr
from pywhatkit import search
import PySimpleGUI as sg
import pyttsx3
from threading import Thread
from time import sleep

r = sr.Recognizer()

layout = [[sg.Text("Search Assistant")], [sg.Button("X")]]

# create window
window = sg.Window("Search Assistant", layout, margins=(500, 300))

# custom thread
# class ThreadWithReturnValue(Thread):
#     def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, Verbose=None):
#         Thread.__init__(self, group, target, name, args, kwargs)
#         self._return = None
#
#     def run(self):
#         if self._target is not None:
#             self._return = self._target(*self._args, **self._kwargs)
#
#     def join(self, *args):
#         Thread.join(self, *args)
#         return self._return
class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self.value = None
    def run(self):
        sleep(1)
        self.value = self._target(*self._args)

#speaking text function
def SpeakText(command):
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()

# listening thread
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
                        return inputText
                        SpeakText(inputText)
                        search(inputText)
        except sr.RequestError as e:
            print("Couldn't recognize results; {0}".format(e))
        except sr.UnknownValueError:
            # if the speech recognizer can't recognize something as speech, it gets caught here
            # print("Unknown error occurred")
            print("Sorry I didn't get that. Please say \"Assistant\" to search.")


# event loop
listenThreadStarted = False
while True:
    event, values = window.read(timeout=100)

    # start listening thread if not started
    if not listenThreadStarted:
        thr = ThreadWithReturnValue(target=listenThread)
        thr.start()

        listenThreadStarted = True



    if event == "X" or event == sg.WIN_CLOSED or thr.value == "EXIT":
        # end thread and program
        thr.join()
        break

window.close()