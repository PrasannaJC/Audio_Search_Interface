
import speech_recognition as sr
from threading import Thread
from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

r = sr.Recognizer()

def Awake():
    awakeFound = False
    while not awakeFound:
        try:
            with sr.Microphone() as source1:
                r.adjust_for_ambient_noise(source1, duration=0.5)
                audio1 = r.listen(source1)
                awakeText = r.recognize_google(audio1)
                awakeText = awakeText.lower()
                print(awakeText)

                if str(awakeText) == "assistant":
                    awakeFound = True
                    print("Exiting ListenForAwake()")
                    return redirect(url_for("listen"))

                    # redirect to next page
        except sr.RequestError as e:
            return "Could not recognize results"
        except sr.UnknownValueError:
            return "Sorry I couldn't understand what you said. Please go back kand try again"

@app.route('/')
def home():
    #thr = Thread(target=Awake)
    #thr.start()
    Awake()
    return render_template("Web_1920___1.html")
    #thr.join()

@app.route('/Web_1920___2.html')
def listen():
    return "success"

if __name__ == "__main__":
    app.run(debug=True)
