#!/usr/bin/env python

import sys
import os
import operator

if len(sys.argv) != 3:
        print("Usage:")
        print("\tparseNames.py names.txt img_folder")
        quit()

with open(sys.argv[1],"r") as f:
        rawText = f.read()

def countPrefixSpaces(line):
        '''counts the number of spaces at the beginning of a line
        '''
        spaces = 0
        for c in line:
                if c == ' ':
                        spaces+=1
                else:
                        # done
                        return spaces
        return spaces

textLines = rawText.split("\n")

# student names begin with some number of spaces (e.g., 11), but we don't know
# how many. So, we'll find the mode of the number of spaces at the beginning
# of each line, and use that.
numSpaces = {}
for line in textLines:
        ps = countPrefixSpaces(line)
        if ps in numSpaces:
                numSpaces[ps]+=1
        else:
                numSpaces[ps]=1

# find the max, ignoring 0, and ignoring any over 20
max_val = 0
max_key = 0
for k,v in numSpaces.iteritems():
        if k > 20 or k == 0:
                continue
        if v > max_val:
                max_val = v
                max_key = k
#print max_key

# only look at lines that start with max_key spaces or blank lines
newText1 = [x[max_key:] for x in textLines if (x.startswith('           ') 
                                         and x[max_key].isalpha()) or len(x)==0]

# read each line until we find two spaces, at which point we truncate
newText1 = [x[:x.find("  ")] for x in newText1]

#for line in newText1:
#        print(line)

# All students will be in the form "something1, something2",
# but there could be two lines that make this up.
# However, there will be a blank line between entries, so if
# there isn't a blank line, then the two should be concatenated
# HOWEVER, there is the unlikely case where two students might not
# have a blank line (double majors...)
# Our final fall-back will be to see if both have a comma, and if so,
# don't put them on the same line, as there will always only be one
# comma per student (hopefully...)

newText2 = []
foundBlank = True

for idx,line in enumerate(newText1):
        if len(line) == 0:
                foundBlank = True
                # now skip
        else:
                if foundBlank: # will always add a new entry if blank was just found 
                        newText2.append(line)
                        foundBlank = False
                else:
                        # make sure both don't have commas 
                        if ',' not in newText2[-1] or ',' not in line:
                                # if prev last character is a comma, put a space
                                # or, if the last character and the first character
                                # are letters, put a space
                                if ((newText2[-1][-1] == ',')
                                   or (newText2[-1][-1].isalpha() and line[0].isalpha())):
                                        newText2[-1]+=' '

                                newText2[-1]+=line
                        else:
                                newText2.append(line)

# remove space after comma and replace with underscore (but leave other spaces)
names = [x.replace(', ','_') for x in newText2]

# now replace names

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

# okay, we can do the renaming
for idx,name in enumerate(names):
       jpg_number = str(idx).zfill(3)
       jpg_name = img_folder+'/image-'+jpg_number+'.jpg'
       new_name = img_folder+'/'+name+'.jpg'
       os.rename(jpg_name,new_name)

