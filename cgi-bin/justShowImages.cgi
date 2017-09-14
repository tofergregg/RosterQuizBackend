#!/usr/bin/env python

import os,sys
import cgitb,cgi
import bcrypt
import subprocess
from subprocess import Popen, PIPE

cgitb.enable()

rosterFolder = 'rosters/'
etcFolder = 'etc/'
pwfile = etcFolder+'pw'
sentinel = '_S__S_' # made this up out of nowhere...

def space_escape(s):
        return s.replace(' ','%20')

def space_unescape(s):
        return s.replace('%20',' ')

form = cgi.FieldStorage()
rosterName = space_escape(form['rosterName'].value)

print("Content-Type:text/html\n")

name = space_escape(form['name'].value)
uploadFile = form['fileToUpload'].value
originalFilename = space_escape(uploadFile)
filename = rosterFolder+name+'/'+rosterName+sentinel+originalFilename

with open('showRoster.html','r') as f:
        outputPage = f.read()

outputPage = outputPage.replace('name=;','name="'+name+'";');
folderName = rosterName+sentinel+originalFilename[:-4]
outputPage = outputPage.replace('imgFolder=;','imgFolder="'+folderName+'";');
print outputPage

