#!/usr/bin/env python

import sys
import os
import operator

BASEDIR = '/afs/cs.stanford.edu/u/cgregg/'
BASEROSTERS = BASEDIR + 'www/rosters/cgi-bin/rosters/'

def printImageToConsole(image):
        # image is a path to an image
        os.system(BASEDIR + "imgcat " + image)

if len(sys.argv) != 3:
        print("Usage:")
        print("\tparseNames.py names.txt img_folder")
        quit()

with open(sys.argv[1],"r") as f:
        names = f.readlines()

# remove newlines from names
names = [x[:-1] for x in names]

img_folder = sys.argv[2]

# names will have the form image-000.jpg and the number will increment by 1
# If all goes well, we will have the same number of files as names
jpgs = os.listdir(img_folder)
jpgs = [x for x in jpgs if ".jpg" in x]

if len(jpgs) != len(names):
        print("Names count and jpg count differ! Quitting!")
        print("Names:%d,Jpegs:%d" % (len(names),len(jpgs)))
        for idx,name in enumerate(names):
                print str(idx+1)+" "+name+"<p>"
        quit()

# print an image, and then rename it based on typed last name
for image,name in zip(jpgs,names):
        printImageToConsole(img_folder+image)
        name = name.replace(', ','_')
        print('"'+name+'"')

        # rename
        os.rename(img_folder+image,img_folder+name+'.jpg')


