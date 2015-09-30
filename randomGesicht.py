#! /usr/bin/python
# -*- coding: utf-8 -*-
import random
import easygui
import sys
import sqlite3
import cv2
import numpy as np

class Gesicht():
    
    optsGesicht = {'Form': ['Viereck', 'Ball', 'Träne', 'Pizza', 'Erdnuss', 'Pyramide', 'Birne', 'Glühbirne'],
           'Gewicht': ['Über', 'Unter', 'Mitte'],
           'Augen': ['V', 'A', 'Horizontal'],
           'Kiefer' : ['Weich', 'Markant'], 
           'Nase' : ['Stups', 'Haken', 'Breit', 'Fein'],
           'Lippen' : ['Voll', 'Dünn'],
           'Augenbrauen' : ['Dick', 'Dünn', 'Hakig'],
           'Haare_Faltpunkt' : ['Stirn, seitlich', 'Stirn, mitte', 'Hinterkopf', 'Seite, tief'],
           'Haare_Pony' : ['Straigth nach unten', 'Buschig nach unten', 'Seitlich konvex', 'Seitlich konkav', 'Mittig, doppelt konkav', 'Straight zurück']}

    optsRandvw = {'Geschlecht': ['Frau', 'Mann'],
                  'Gefuehl': ['Froh', 'Überrascht', 'Wütend', 'Flirty', 'Entschlossen', 'Friedlich', 'Jammernd'],
                  'Blickrichtung': ['O', 'OR', 'R', 'UR', 'U', 'UL', 'L', 'OL']}

    auswahl = {}

    def __init__(self):
        
        for opt, werte in self.optsGesicht.iteritems():
            rn = random.randrange(0,len(werte)-1)
            self.auswahl[opt] = werte[rn]

        for opt, werte in self.optsRandvw.iteritems():
            rn = random.randrange(0,len(werte)-1)
            self.auswahl[opt] = werte[rn]



def preprocess(imgname):
    img = cv2.imread(imgname)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray,(5,5),0)
    img_hist = img_blur #cv2.equalizeHist(img_blur)
    (thrshld, img_thr) = cv2.threshold(img_hist,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    return img_thr

def saveImg(img_arr, anna):

    dic = anna.auswahl
    dic["id"] = None
    dic["Bild"] = img_arr.dumps() // Kann zurück ausgelesen werden mit numpy.loads(dmp)
    keys = ','.join(dic.keys())
    vals = ','.join(dic.values())
    sql = "INSERT INTO rgtable (%s) VALUES (%s)" % (keys, vals)
    cur.execute(sql)


redraw = ''
path = "/home/michael/codes/python_codes/randomGesicht/bilder/"
con = sqlite3.connect('rgdb.db')
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS rgtable (
                                    id INTEGER PRIMARY KEY, 
                                    Bild text,
                                    Form CHAR(20),
                                    Gewicht CHAR(20),
                                    Augen CHAR(20),
                                    Kiefer CHAR(20),
                                    Nase CHAR(20),
                                    Lippen CHAR(20),
                                    Augenbrauen CHAR(20),
                                    Haare_Faltpunkt CHAR(50),
                                    Haare_Pony CHAR(50),
                                    Geschlecht CHAR(1),
                                    Gefuehl CHAR(20),
                                    Blickrichtung CHAR(2))''')




if __name__ == "__main__":
    while 1:

        text = "Willkommen zu Michaels Gesichter-Trainer!"
        auswahl = ['Neues Gesicht', 'Hochladen', 'Beenden']

        if redraw == '':
            redraw = easygui.buttonbox(text, choices = auswahl)
        
        if redraw == 'Neues Gesicht':
            anna = Gesicht()
            text += "\n Anna erzeugt!"
            for opt, wert in anna.auswahl.iteritems():
                text += "\n %s : %s" % (opt, wert)
            redraw = easygui.buttonbox(text, choices = auswahl)

        if redraw == 'Hochladen':
            msg = "Bitte lade das Bild hoch!"
            title = "Bild auswählen"
            imgname = easygui.fileopenbox(msg, title, default='*', filetypes = "*.jpg", multiple=False)
            img_arr = preprocess(imgname)
            saveImg(img_arr, anna)

        if redraw == 'Beenden':
            sys.exit(0)
            
        
