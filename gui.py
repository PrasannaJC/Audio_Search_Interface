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

sz=(15,10)
col1=[[sg.Text("", font=('Helvetica', 40), justification='center', size=(15,14))]]
col2=[
    [sg.Text("Search Assistant", font=('Helvetica', 40), justification='center', key='titleText_1', size=(15,4))],
    [sg.Text("", font=('Helvetica', 40), justification='center', key='titleText_2', size=(15,4))],
    [sg.Text("Please say \"Assistant\" to begin.", font=('Helvetica', 40), justification='center', key='titleText_3', size=(15,3))],
    [sg.Text("", font=('Helvetica', 40), justification='center', key='titleText_4', size=(17,3))]
]
col3=[
    [sg.Image(size=(10,10), key='image_1')],
    [sg.Text("", font=('Helvetica', 40), justification='center', key='rightColText', size=(15,12))],
]


layout = [[
    sg.Column(col1, element_justification='c'),
    sg.Column(col2, element_justification='c'),
    sg.Column(col3, element_justification='c')
]]


# create window
window = sg.Window("Search Assistant", layout, )

# custome thread class to return value from individual thread
class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self.value = None
    def run(self):
        sleep(1)
        self.value = self._target(*self._args)

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
        window['titleText_2'].update('Assistant Ready', text_color='green')
        window['titleText_3'].update('Please say what you would\n like to search for', text_color="white")
        window['rightColText'].update('Say\n"End Program"\n to exit')
        window['image_1'].update('redX.png')
        # spin off listen for search thread
        thr = ThreadWithReturnValue(target=listenForSearchThread, args=(mic, r))
        thr.start()
        #thr.join()

    if thr.value != None and thr.value != "yes" and thr.value != "no" and thr.value != "EXIT" and thr.value != "end program":
        window['titleText_2'].update('I heard ...', text_color="white")
        window['titleText_3'].update(thr.value, text_color="black")
        window['titleText_4'].update("Say \"Yes\" to search.\nSay \"No\" to try again.")
        #spin off confirmation thread
        thr = ThreadWithReturnValue(target=validationThread, args=(mic, r, thr.value))
        thr.start()
    elif thr.value == "end program":
        thr.join()
        break

    #print("RETURN FROM VALIDATION THREAD:" + str(thr.value))

    if thr.value == "no":
        window['titleText_2'].update('Assistant Ready', text_color='green')
        window['titleText_3'].update('Please say what you would\n like to search for', text_color="white")
        window['titleText_4'].update("")
        # spin off listen for search thread
        thr = ThreadWithReturnValue(target=listenForSearchThread, args=(mic, r))
        thr.start()

    if thr.value == "yes":
        window['titleText_2'].update("")
        window['titleText_3'].update("Please say \"Assistant\" to begin.", text_color="white")
        window['titleText_4'].update("")
        window['image_1'].update("")
        window['rightColText'].update("")
        #spin off initial awake thread
        thr = ThreadWithReturnValue(target=awakeThread, args=(mic, r))
        thr.start()

    if thr.value == "EXIT":
        thr.join()
        break



    if event == "X" or event == sg.WIN_CLOSED or thr.value == "EXIT":
        # end thread and program
        thr.join()
        break

window.close()