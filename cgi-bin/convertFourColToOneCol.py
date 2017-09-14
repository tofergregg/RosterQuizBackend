#!/usr/bin/env python

import sys

def fillNonRuns(runs):
        '''this takes a name runs list and adds "None"
        for columns that are not present, based on
        the rough ranges of a column being in the range 0-24,25-49,50-74,75-
        '''
        # if there are already 4 columns, don't try and guess them
        if len(runs) == 4:
                return runs
        newRuns = [None] * 4 
        for run in runs:
                # use midpoint of run
                midpoint = (run[0] + run[1]) / 2
                if midpoint < 20:
                        newRuns[0] = run
                elif midpoint < 45:
                        newRuns[1] = run
                elif midpoint < 70:
                        newRuns[2] = run
                else:
                        newRuns[3] = run
        return newRuns

def nameRunsOnLine(line):
        ''' returns a tuple in the following form:
        ((0,24),(28,50),(57-72),(76-85))
        Where each inner tuple are the columns that
        match names, which should have multiple
        spaces between them. Sometimes, however
        we have a case where a name break is only
        a single space, so we have to make a guess at
        the nearest space on either side.

        A typical name line could be:
          Sunny Xiaoran Li            Yue Li               JC Liang             Lisa C Liao

        Where each name is nicely separated by more than one space.

        But it could also be:
          Aprotim Cory Bhowmik Alessandra Venezia Blanco    Jenia Borisenko           Stephanie Danielle Brito

        Note that there is only one space between "Browmik" and "Alessandra",
        even though they are a last name and then a first name. Yuck.

        This should also return None for columns that do not exist,
        based on the rough ranges of a column being in the range 0-24,25-49,50-74,75-

        e.g.,
        (None,None,(57-72),None)
        for a third-column-only line
        '''
        # find the text runs, ignoring single spaces 
        runs = []
        inRun = False
        prevIsSpace = False # no spaces yet
        for idx,c in enumerate(line):
                if c != ' ':
                        prevIsSpace = False
                        if not inRun:
                                inRun = True
                                runStart = idx
                else:
                        if inRun and prevIsSpace: 
                                # we found the end, but only if
                                # there is more than one space
                                runs.append((runStart,idx-2))
                                inRun = False
                        prevIsSpace = True
        # catch the last one if necessary
        if inRun:
                runs.append((runStart,len(line)-1))

        # fill in non-runs
        return fillNonRuns(runs)

def namesOnLine(line):
        runs = nameRunsOnLine(line)
        names = []
        for run in runs:
                if run == None:
                        names.append('')
                else:
                        names.append(line[run[0]:run[1]+1])
        return names
if len(sys.argv) < 2:
        print("usage:\n\t./convertFourColToTwoCol.py roster.txt")
        quit()


with open(sys.argv[1]) as f:
        fullText = f.read()

# convert ^L to four newlines
cleanText = ""
for c in fullText:
        if c == '':
                cleanText += '\n\n\n\n'
        else:
                cleanText += c

col0 = ""
col1 = ""
col2 = ""
col3 = ""

for line in cleanText.split('\n'):
        if line == "":
                continue
        nameRuns = namesOnLine(line)
        col0 += nameRuns[0]+'\n'
        col1 += nameRuns[1]+'\n'
        col2 += nameRuns[2]+'\n'
        col3 += nameRuns[3]+'\n'


singleCol = col0 + col1 + col2 + col3

# do some replacement to find photo not available
singleCol = singleCol.replace("Photo\nNot\nAvailable\n","Photo Not Available:")

print singleCol
