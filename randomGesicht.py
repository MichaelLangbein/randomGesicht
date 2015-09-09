# -*- coding: utf-8 -*-
import random
import easygui
import sys

class Gesicht():
    
    optsGesicht = {'Form': ['Viereck', 'Ball', 'Träne', 'Pizza', 'Erdnuss', 'Pyramide'],
           'Gewicht': ['Über', 'Unter', 'Mitte'],
           'Augen': ['V', 'A', 'Horizontal'],
           'Kiefer' : ['Weich', 'Markant']}

    optsRandvw = {'Geschlecht': ['Frau', 'Mann'],
                  'Gefühl': ['Froh', 'Überrascht', 'Wütend', 'Flirty'],
                  'Blickrichtung': ['O', 'OR', 'R', 'UR', 'U', 'UL', 'L', 'OL']}

    auswahl = {}

    def __init__(self):
        
        for opt, werte in self.optsGesicht.iteritems():
            rn = random.randrange(0,len(werte)-1)
            self.auswahl[opt] = werte[rn]

        for opt, werte in self.optsRandvw.iteritems():
            rn = random.randrange(0,len(werte)-1)
            self.auswahl[opt] = werte[rn]


if __name__ == "__main__":
    while 1:

        text = "Willkommen zu Michaels Gesichter-Trainer!"
        auswahl = ['Neues Gesicht', 'Beenden']
        redraw = easygui.buttonbox(text, choices = auswahl)
        
        if redraw == 'Neues Gesicht':
            anna = Gesicht()
            text += "Anna erzeugt!"    
            redraw = easygui.buttonbox(text, choices = auswahl)

        if redraw == 'Beenden':
            sys.exit(0)
        
