#!/usr/bin/env python

import os
import sys
import subprocess
import tempfile

if len(sys.argv) != 3:
        print("Usage:")
        print("\tnoPhotosList.py roster.pdf names.txt")
        quit()

rosterPdf = sys.argv[1]
namesFile = sys.argv[2]

# extract text from the PDF
tmpNames = tempfile.mktemp()
os.system("pdftotext -layout "+rosterPdf+" "+tmpNames)

# convert the columns and extract Photo Not Available lines

proc = subprocess.Popen(["./convertFourColToOneCol.py",tmpNames], stdout=subprocess.PIPE)
(out, err) = proc.communicate()

noPhotoNames = [x for x in out.split('\n') if 'Photo Not Available' in x]
noPhotoNames = [x.split(':')[1] for x in noPhotoNames]
noPhotoNames = [sorted(x.replace(',','').split(' ')) for x in noPhotoNames]

# now read in the text roster and find those names
with open(namesFile) as f:
        names = f.read().split('\n')

noPhotoRosterNames = []
for noPhotoName in noPhotoNames:
        for name in names:
                # split the name by spaces, and get rid of the commas
                sortedName = sorted(name.replace(',','').split(' '))
                if (sortedName == noPhotoName):
                        print(name)
