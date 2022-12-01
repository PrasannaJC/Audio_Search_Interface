# file for managing gui settings

import PySimpleGUI as sg
import speech_recognition as sr
from pywhatkit import search
import PySimpleGUI as sg
import pyttsx3
from threading import Thread
from time import sleep

from Utils import *

r = sr.Recognizer()
mic = sr.Microphone()

#starting screen layout
# layout = [
#     [sg.Text("Search Assistant", font=('Helvetica', 40), justification='center', key='titleText_1')],
#     [sg.Text("Please say \"Assistant\" to begin.", font=('Helvetica', 20), justification='center', key='titleText_2')],
# ]

sz=(15,10)
col1=[[sg.Text("", font=('Helvetica', 40), justification='center', background_color='red', size=(4,12))]]
col2=[
    [sg.Text("Search Assistant", font=('Helvetica', 40), justification='center', key='titleText_1', background_color='green', size=(15,4))],
    [sg.Text("", font=('Helvetica', 40), justification='center', key='titleText_2', background_color='green', size=(15,4))],
    [sg.Text("Please say \"Assistant\" to begin.", font=('Helvetica', 40), justification='center', key='titleText_3', background_color='green')],
    [sg.Text("", font=('Helvetica', 40), justification='center', key='titleText_4', background_color='green')]
]
col3=[[sg.Text("", font=('Helvetica', 40), justification='center', background_color='blue', size=(4,12))]]

layout = [[
    sg.Column(col1, element_justification='c'),
    sg.Column(col2, element_justification='c'),
    sg.Column(col3, element_justification='c')
]]


# create window
window = sg.Window("Search Assistant", layout, )

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

# #speaking text function
# def SpeakText(command):
#     engine = pyttsx3.init()
#     engine.say(command)
#     engine.runAndWait()

# listening thread
# def listenThread():
#     while True:
#         try:
#             with sr.Microphone() as source1:
#                 r.adjust_for_ambient_noise(source1, duration=0.5)
#                 audio1 = r.listen(source1)
#                 awakeText = r.recognize_google(audio1)
#                 awakeText = awakeText.lower()
#
#                 print(awakeText)
#                 # "assistant" check - user wants to search something
#                 if str(awakeText) == "assistant":
#                     return(awakeText)
#                     print("Please say your command...")
#                     searchText = r.listen(source1)
#
#                     inputText = r.recognize_google(searchText)
#                     inputText = inputText.lower()
#
#                     print("Did you say: \"" + inputText + "\"")
#
#                     if str(inputText) == "end program":
#                         # raise SystemExit()
#                         return "EXIT"
#                     print("Respond with either 'YES' or 'NO")
#
#                     audio2 = r.listen(source1)
#                     inputVerify = r.recognize_google(audio2)
#                     inputVerify = inputVerify.lower()
#                     print(inputVerify)
#                     if str(inputVerify) == "yes":
#                         SpeakText(inputText)
#                         search(inputText)
#                         #return inputText
#         except sr.RequestError as e:
#             print("Couldn't recognize results; {0}".format(e))
#         except sr.UnknownValueError:
#             # if the speech recognizer can't recognize something as speech, it gets caught here
#             # print("Unknown error occurred")
#             print("Sorry I didn't get that. Please say \"Assistant\" to search.")


# event loop
listenThreadStarted = False
while True:
    event, values = window.read(timeout=100)

    # start listening thread if not started
    if not listenThreadStarted:
        thr = ThreadWithReturnValue(target=awakeThread, args=(mic, r))
        thr.start()

        listenThreadStarted = True

    if thr.value == 'assistant':
        window['titleText_2'].update('Assistant Ready')
        window['titleText_3'].update('Please say what you would\n like to search for')
        # spin off listen for search thread
        thr = ThreadWithReturnValue(target=listenForSearchThread, args=(mic, r))
        thr.start()
        #thr.join()

    if thr.value != None:
        window['titleText_2'].update('I heard ...')
        window['titleText_3'].update(thr.value)
        window['titleText_4'].update("Say \"Yes\" to search, or \"No\" to try again.")
        #spin off confirmation thread
        thr = ThreadWithReturnValue(target=validationThread, args=(mic, r, thr.value))

        thr.start()
        #print("RETURN FROM VALIDATION THREAD:" + str(thr.value))





    if event == "X" or event == sg.WIN_CLOSED or thr.value == "EXIT":
        # end thread and program
        thr.join()
        break

window.close()