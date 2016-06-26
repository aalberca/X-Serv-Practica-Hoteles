#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# Simple XML parser for the RSS channel from BarraPunto
# Jesus M. Gonzalez-Barahona
# jgb @ gsyc.es
# TSAI and SAT subjects (Universidad Rey Juan Carlos)
# September 2009
#
# Just prints the news (and urls) in BarraPunto.com,
#  after reading the corresponding RSS channel.

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
import urllib2

class myContentHandler(ContentHandler):

    def __init__ (self):
        self.incategoria = False
        self.insubcategoria = False
        self.inContent = True
        self.theContent = ""
        self.line = ""
        self.enlace = ""
        self.lista_fotos = []
        self.hotel = {}
        self.lista_hoteles = []

    def startElement (self, name, attrs):
    
        if name == 'service':
            if len(self.hotel) != 0:
                self.lista_hoteles.append(self.hotel)
                self.hotel = {}
        elif name == 'item' and attrs.get('name') == 'Categoria':
            self.incategoria = True
        elif name == 'item' and attrs.get('name') == 'SubCategoria':
            self.insubcategoria = True


    def endElement (self, name):

        if name == 'multimedia':
            self.inmultimedia = False
            self.hotel['url_fotos'] = self.lista_fotos # solo anado la lista al diccionario al final de todas las urls
            self.lista_fotos = []
        elif name == 'url':
            self.lista_fotos.append(self.theContent)
        elif self.incategoria:
            self.hotel["Categoria"] = self.theContent
            self.theContent = ""
            self.incategoria = False
        elif self.insubcategoria:
            self.hotel["SubCategoria"] = self.theContent
            self.theContent = ""
            self.insubcategoria = False
        else:
            if self.theContent != '':
                self.hotel[name] = self.theContent
            self.theContent = ""

    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars


    def devuelve_lista (self):
        return self.lista_hoteles

# Load parser and driver
def parsear_fichero (fichero):
        #Load parser and driver
    theParser = make_parser()
    theHandler = myContentHandler()
    theParser.setContentHandler(theHandler)
    # Ready, set, go!
    archivo = urllib2.urlopen(fichero)
    theParser.parse(archivo)
    datos_hoteles = theHandler.devuelve_lista()
    return datos_hoteles

#print "Parse complete"
