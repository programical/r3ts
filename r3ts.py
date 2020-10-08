#!/usr/bin/env python3


from time import sleep
from threading import Thread
from appJar import gui
import pyttsx3


class R3TS:
    def __init__(self):
        # tts setup
        self.tts = pyttsx3.init()
        self.busy = False
        self.endChars = (' ', '.', ',', '!', '?')

        # window setup
        self.app = gui(showIcon = False)
        self.app.setTitle('R3TS')

        # WPM scale setup
        self.app.addLabelScale('WPM')
        self.app.setScaleChangeFunction('WPM', self.setSpeed)
        self.app.setScaleRange('WPM', 60, 300)
        self.app.setScaleIncrement('WPM', 10)
        self.app.showScaleIntervals('WPM', 120)
        self.app.setScale('WPM', 180, callFunction = True)

        # volume scale setup
        self.app.addLabelScale('Volume')
        self.app.setScaleChangeFunction('Volume', self.setVolume)
        self.app.setScaleRange('Volume', 0, 100)
        self.app.setScaleIncrement('Volume', 10)
        self.app.showScaleIntervals('Volume', 50)
        self.app.setScale('Volume', 50, callFunction = True)

        # voice options setup
        voiceOptions = []
        for voice in self.tts.getProperty('voices'):
            voiceOptions.append(str(voice.id) + ' ::: ' + str(voice.gender))

        self.app.addLabelOptionBox('Voice', voiceOptions)
        self.app.setOptionBox('Voice', 0, callFunction = True)
        self.app.setOptionBoxChangeFunction('Voice', self.setVoice)

        # text input setup
        self.app.addEntry('Words')
        self.app.setEntry('Words', '', callFunction = True)
        self.app.setEntryChangeFunction('Words', self.speakWord)

    def go(self):
        self.app.go()

    # change event function of text input
    def speakWord(self, entryId):
        text = self.app.getEntry(entryId)
        # if busy, ignore event, try next time
        if text.endswith(self.endChars) and not self.busy:
            self.spawnSpeechThread()

    # clears input and spawns speech thread
    def spawnSpeechThread(self):
        text = self.app.getEntry('Words')
        self.busy = True
        self.app.setEntry('Words', '')
        Thread(target = self.speechThread, args = (text,)).start()

    # threading must be used to prevent freezing the text input
    def speechThread(self, word):
        self.tts.say(word)
        self.tts.runAndWait()

        # start next one right away if possible
        # helpful when sentence-ending word is in queue
        newText = self.app.getEntry('Words')
        if newText.endswith(self.endChars):
            self.spawnSpeechThread()
        else:
            self.busy = False

    # change event function of WPM slider
    def setSpeed(self, scaleId):
        speed = self.app.getScale(scaleId)
        self.tts.setProperty('rate', speed)

    # change event function of voice select
    def setVoice(self, optionsId):
        # ::: is a bad hack, don't try this at home
        self.tts.setProperty('voice', self.app.getOptionBox('Voice').split(' ::: ')[0])

    # change event function of volume slider
    def setVolume(self, scaleId):
        self.tts.setProperty('volume', self.app.getScale('Volume') / 100.0)


def main():
    R3TS().go()


if __name__ == '__main__':
    main()
