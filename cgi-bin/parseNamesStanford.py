#!/usr/bin/env python

import sys,os
from shutil import copyfile
from shutil import move

def photo_positions(line):
    ''' Determine the location of any "Photo" words on a line.
        There could be up to four positions, and there will be a range
        of positions. E.g., at the first and fourth position:
        "        Photo                                                                         Photo"
        returns a 4-tuple of true or false values depending on the position
    '''
    positions = [False]*4 # start with all falses
    i = 0 # start of string
    while i != -1:
        i = line.find('Photo',i+1) # we shouldn't have a case where it is the first character
        if i != -1:
            # assume first location < 15
            if i < 15:
                positions[0] = True
            # assume 20 <= second location < 50
            elif i >= 20 and i < 50:
                positions[1] = True
            # assume 50 <= third location < 70
            elif i >= 50 and i < 70:
                positions[2] = True
            # assume third position >= 70
            elif i >= 70:
                positions[3] = True
    return tuple(positions)

def noPhotoNames(line,positions):
    ''' Takes a line with student names separated by two or more spaces and a
        tuple of positions, and returns a tuple with the student names
    '''
    names = []
    for i in range(4):
        line = line.lstrip() # strip leading spaces
        # find position of double space (or end of line)
        space_pos = line.find('  ')
        if space_pos != -1:
            name = line[:space_pos]
            # update line to remove this name
            line = line[space_pos+2:]
        else:
            name = line # the rest of the line
        if positions[i]:
            names.append(name)
    return tuple(names)

def getNames(filename):
    #with open(filename,'r',encoding='utf-8') as f:
    with open(filename,'r') as f:
        lines = f.readlines()

    # remove newlines
    lines = [x[:-1] for x in lines]

    # remove blank lines
    lines = [x for x in lines if x != '']

    # remove ctrl-L if necessary
    lines = [x.replace('\x0c','') for x in lines]
    allNames = ()

    lineNo = 0 # first line
    while lineNo < len(lines):
        line = lines[lineNo]
        #print("'%s'" % line)
        if 'Photo' in line:
            positions=photo_positions(line)
            # now read the third line down (the other two lines say "Not" and "Available"
            lineNo+=3
            names = noPhotoNames(lines[lineNo],positions)
            allNames += names
        lineNo+=1
    return allNames

def studentPhotoNames(filename):
    #with open(filename,'r',encoding='utf-8') as f:
    with open(filename,'r') as f:
        lines = f.readlines()
    # remove lines that start with "Download"
    #  or "Print"
    #  or "All Sections" 
    lines = [x for x in lines if not x.startswith("Download")]
    lines = [x for x in lines if not x.startswith("Print")]
    lines = [x for x in lines if not x.startswith("All Sections")]

    '''
    newLines = []
    foundSentinel = False
    for line in lines:
        if not foundSentinel:
                if 'Download' in line:
                        foundSentinel = True
                continue
        newLines.append(line)
    lines = newLines
    '''
    # remove newlines from end of each line
    lines = [x[:-1] for x in lines]
    # remove ctrl-Ls
    lines = [x.replace('\x0c','') for x in lines]
    # remove blank lines
    #lines = [x for x in lines if x != '']
    # remove "Photo Not Available" lines
    lines = [x for x in lines if not x.startswith("Photo")]
    lines = [x for x in lines if not x.startswith("Not")]
    lines = [x for x in lines if not x.startswith("Available")]

    # concatenate lines that do not have a newline between them
    lineNo = 0
    lines2 = []
    lastLineNew = True
    for line in lines:
        if (line != ''):
            if lastLineNew:
                lines2.append(line)
                lastLineNew = False
            else:
                lines2[-1]+=' '+line
        else:
            lastLineNew = True
    lines = lines2
    # the following is a huge kludge
    # Sometimes, two students with long names will end up getting
    # parsed as a single student, because their names end up next
    # to each other in the PDF, and pdftotext can't distinguish them
    # So, we'll search for names longer than 40 characters long (emperically
    # determined...), and split them at a space that is nearest to
    # the center. Not sure of a better solution, although we could
    # potentially leverage the layout roster to figure this out
    namesToInsert = [] # we need to insert these names
                       # (we can't do this while iterating)
    for idx,line in enumerate(lines):
            if len(line) > 40:
                    # find the space closest to the middle and break there
                    forward = True # the direction to search
                    middle = len(line) / 2 # start at the middle
                    pos = middle # the current search location
                    count = 0 # how many away we've searched
                    while True: # keep searching until we find a space
                        if line[pos] == ' ': # found a space!
                                name1 = line[:pos]
                                name2 = line[pos+1:]
                                namesToInsert.append((idx,name1,name2))
                                break
                        else:
                                if forward:
                                        pos = middle + count
                                        forward = False
                                else:
                                        pos = middle - count
                                        forward = True
                        count += 1
    # insert the names into a new list, if necessary
    print("Remaining names: ")
    print(namesToInsert)
    if len(namesToInsert) > 0:
            lines2 = []
            nextNameToInsert = namesToInsert[0]
            namesToInsert = namesToInsert[1:] # basically, pop first into nextNameToInsert
            for idx,line in enumerate(lines):
                    if nextNameToInsert != None and idx == nextNameToInsert[0]:
                        lines2.append(nextNameToInsert[1])
                        lines2.append(nextNameToInsert[2])
                        if len(namesToInsert) > 0:
                            nextNameToInsert = namesToInsert[0]
                            namesToInsert = namesToInsert[1:] # basically, pop first into nextNameToInsert
                    else:
                        lines2.append(line)

            lines = lines2

    return lines

def firstImageNum(imageDir):
    '''Returns the number of the first image'''
    files = os.listdir(imageDir)
    files = [x for x in files if 'jpg' in x]
    files = [x.replace('image-','').replace('.jpg','') for x in files]
    files.sort()
    return int(files[0])
def renameImages(allNames,noPhotoStudents,imageDir):
    imageNo = firstImageNum(imageDir) # start with the first image
    # remove those images
    #os.remove(imageDir+'image-000.jpg')
    #os.remove(imageDir+'image-001.jpg')
    for name in allNames:
        skipName = False
        for noPhotoName in noPhotoStudents:
            if noPhotoName in name:
                # replace with blank image
                nameParts = name.split(' ')
                first = nameParts[0]
                last = nameParts[-1]
                copyfile('User-400.jpg',imageDir+last+'_'+first+'.jpg')
                skipName = True
        if not skipName:
            # replace with actual name
            # use last,first (not perfect)
            nameParts = name.split(' ')
            first = nameParts[0]
            last = nameParts[-1]
            imageName=imageDir+'image-%03d.jpg' % imageNo
            move(imageName,imageDir+last+'_'+first+'.jpg')
            imageNo+=1


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage:")
        print("\tparseNamesStanford.py names_layout.txt names_no_layout.txt img_folder")
        quit()

    # get the names of students with no photos
    noPhotoStudents = getNames(sys.argv[1])
    #print(noPhotoStudents)
    allNames = studentPhotoNames(sys.argv[2])
    #print(allNames)
    renameImages(allNames,noPhotoStudents,sys.argv[3])
