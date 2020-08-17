#!/usr/bin/python
import os
from multiprocessing import Process
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtGui import QIcon, QImage, QPixmap
from PyQt5.QtWidgets import QGridLayout, QWidget, QDesktopWidget
import sys
import wolframalpha # Wolfram Alpha API (THE BRAINS!!!)
from gtts import gTTS # Speech Synthesis
from io import BytesIO
#import pyttsx3
import pygame
import speech_recognition as sr 
import random 
from playsound import playsound # Media Player

r = sr.Recognizer()
#engine = pyttsx3.init()
#rate = engine.getProperty('rate')
#engine.setProperty('rate', 190)
#voices = engine.getProperty('voices')
#engine.setProperty('voice', voices[1].id)
app_id = "Q52YQA-HQH6T3GK9J"

def say(text):
    tts = gTTS(text, lang='en')
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    pygame.mixer.init()
    pygame.mixer.music.load(fp)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
exit = 0

def on_exit():
    os._exit(os.EX_OK)

def Ui():
    app = QtWidgets.QApplication([])
    win = uic.loadUi('VA.ui')
    win.show()
    qtRec = win.frameGeometry()
    qtRec.moveCenter(QDesktopWidget().availableGeometry().center())
    win.move(qtRec.topLeft())
    brainsImg = QImage('brain.svg')
    brainsImg = brainsImg.scaled(195, 195, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.SmoothTransformation)
    win.Brains.setPixmap(QPixmap.fromImage(brainsImg))
    win.exitbtn.clicked.connect(on_exit)
    sys.exit(app.exec())

def VirtualAssistant():
    say("      virtual assistant activated")
    while True:
        with sr.Microphone() as source:
            ans = ["  What's up?", "  What do you need?", "  What can I do for you?"] # Catalog of phrases after trigger 
            wait = ["  Give me a second while I think.", "  Ok thinking"] # Catalog of phrases after command
            random_ans = random.choice(ans) # Randomizes answer phrase choice
            random_wait = random.choice(wait) #  Randomizes wait phrase choice
            try:
                r.adjust_for_ambient_noise(source) # Adjusts audio input for improved speech recognition
                audio = r.listen(source) # Listens for voice
                if r.recognize_google(audio) == "Sarah": # Trigger (What the Assistant answer to) // Also checks for trigger
                    playsound('ding.mp3') 
                    say(random_ans) #engine.say(random_ans)
                    print("Sarah: "+random_ans)
                    #engine.runAndWait()
                    prompted = 1
                    while prompted == 1:
                        audio = r.listen(source)
                        if r.recognize_google(audio) == "nevermind":
                            print("You: "+r.recognize_google(audio))
                            say("  Ok Bye.") #engine.say("Ok Bye.")
                            print("Sarah: "+"Ok Bye.")
                            #engine.runAndWait()
                            prompted = 0
                        else:
                            print("You: "+r.recognize_google(audio))
                            say(random_wait) #engine.say(random_wait)
                            print("Sarah: "+random_wait)
                            #engine.runAndWait()
                            client = wolframalpha.Client(app_id)
                            res = client.query(r.recognize_google(audio))
                            print("Sarah: "+next(res.results).text)
                            say(next(res.results).text) #engine.say(next(res.results).text)
                            #engine.runAndWait()
                            prompted = 0
            except sr.UnknownValueError as uval:
                print(uval)

def main():
    p1 = Process(target = Ui)
    p1.start()
    p2 = Process(target = VirtualAssistant)
    p2.start()

if __name__ == "__main__":
    main()