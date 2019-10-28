#!/usr/bin/python3

from time import sleep
from threading import Thread
from appJar import gui
import pyttsx3

# change event function of text input
def speakWord(entryId):
    text = app.getEntry(entryId)
    if " " in text:
        app.setEntry("Words", "")
        Thread(target=speechThread, args=(text,)).start()

# threading must be used to prevent freezing the text input
def speechThread(word):
    while True:
        try:
            sleep(0.2) # I don't know why this needs a delay, but it does bad stuff without it
            tts.say(word)
            tts.runAndWait()
            break
        except RuntimeError:
            pass

# change event function of WPM slider
def setSpeed(scaleId):
    speed = app.getScale(scaleId)
    tts.setProperty("rate", speed)

# change event function of voice select
def setVoice(optionsId):
    tts.setProperty("voice", app.getOptionBox("Voice").split(": ")[0])

# change event function of volume slider
def setVolume(scaleId):
    tts.setProperty("volume", app.getScale("Volume")/100.0)

# tts
tts = pyttsx3.init()

# window setup
app = gui(showIcon=False)
app.setTitle("R3TS")

# WPM scale setup
app.addLabelScale("WPM")
app.setScaleChangeFunction("WPM", setSpeed)
app.setScaleRange("WPM", 60, 300)
app.showScaleIntervals("WPM", 120)
app.setScale("WPM", 180, callFunction=True)

# volume scale setup
app.addLabelScale("Volume")
app.setScaleChangeFunction("Volume", setVolume)
app.setScaleRange("Volume", 0, 100)
app.showScaleIntervals("Volume", 50)
app.setScale("Volume", 50, callFunction=True)

# voice options setup
voiceOptions = []
for voice in tts.getProperty("voices"):
    voiceOptions.append(str(voice.id) + ": " + str(voice.gender))

app.addLabelOptionBox("Voice", voiceOptions)
app.setOptionBox("Voice", 0, callFunction=True)
app.setOptionBoxChangeFunction("Voice", setVoice)

# text input setup
app.addEntry("Words")
app.setEntry("Words", "", callFunction=True)
app.setEntryChangeFunction("Words", speakWord)

app.go()
