#!/usr/bin/env python

import sys
import os
import operator
import subprocess
from shutil import copyfile,rmtree

BASEDIR = '/afs/cs.stanford.edu/u/cgregg/'
BASEROSTERS = BASEDIR + 'www/rosters/cgi-bin/rosters/'

def printImageToConsole(image):
        # image is a path to an image
        os.system(BASEDIR + "imgcat " + image)

def simplifyName(name):
        nameForImage = name.replace(', ','_')
        # attempt to take out middle name by
        # finding the first space after the underscore
        indexOfSpace = nameForImage.find(' ',nameForImage.find('_'))
        if indexOfSpace != -1: # -1 means that there isn't a middle name
                nameForImage = nameForImage[:indexOfSpace]
        nameForImage = nameForImage+'.jpg'
        return nameForImage


if len(sys.argv) != 4:
        print("Usage:")
        print("\tmatchImages.py roster.pdf names.txt img_folder")
        quit()
pdf_file = sys.argv[1]
roster_names = sys.argv[2]
img_folder = sys.argv[3]+"/" # in case the user forgot


# extract the images from the PDF
# check if img_folder exists, if not, create it
if not os.path.exists(img_folder):
        os.makedirs(img_folder)
else:
        # remove everything in the directory
        rmtree(img_folder)
        os.makedirs(img_folder)

# extract the images
os.system("pdfimages -j "+pdf_file+" "+img_folder+"image")

# remove the .ppm images
allImages = os.listdir(img_folder)
allImages = [x for x in allImages if ".jpg" not in x]
for image in allImages:
        os.remove(img_folder+"/"+image)

with open(roster_names,"r") as f:
        names = f.readlines()

# remove newlines from names
names = [x[:-1] for x in names]

img_folder = img_folder 

# we need to see if there are any missing jpgs (for Stanford PDFs)

proc = subprocess.Popen(["./noPhotosList.py",pdf_file,roster_names], stdout=subprocess.PIPE)
(noPhotosNames, err) = proc.communicate()
noPhotosNames = noPhotosNames.split('\n')[:-1]

# If all goes well, we will have the same number of files as names
jpgs = os.listdir(img_folder)
jpgs = [x for x in jpgs if ".jpg" in x]

if len(jpgs)+len(noPhotosNames) != len(names):
        print("Names count and jpg count differ! Quitting!")
        print("Names:%d,Jpegs:%d" % (len(names),len(jpgs)+len(noPhotosNames)))
        for idx,name in enumerate(names):
                print str(idx+1)+" "+name+"<p>"
        quit()

# print an image, and then rename it based on typed last name
noImageCount = 0
for idx,name in enumerate(names):
        nameForImage = simplifyName(name)
        if name in noPhotosNames:
                image = "User-400.jpg" # blank image
                # copy image file
                copyfile(image,img_folder+nameForImage)
                noImageCount += 1
        else:
                image = jpgs[idx - noImageCount] 
                # rename
                os.rename(img_folder+image,img_folder+nameForImage)
        #printImageToConsole(img_folder+image)
        #print('"'+name+'"')



