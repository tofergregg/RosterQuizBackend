#!/bin/bash

if [ "$#" -ne 2 ]; then
            echo "Usage:"
            printf "\t./extractImages.sh pdf_file image_dir\n"
            exit -1
fi

# set up image directory

filename=$1
imageDir=$2

# create directory and empty it
mkdir ${imageDir} 2> /dev/null
rm ${imageDir}/* 2> /dev/null

# convert the images
./convertImages.sh ${filename} ${imageDir}

# extract the text from the pdf
pdftotext -layout ${filename} ${imageDir}/roster.txt 

# Stanford PDFs will have a defining "Print" on the first or second line
head -n2 ${imageDir}/roster.txt | grep "Print" > /dev/null
if [[ $? == 0 ]]; then 
        # extract a non-layout version as well
        #echo "Stanford PDF"
        # remove any ppms
        rm ${imageDir}/*.ppm 2>/dev/null
        pdftotext ${filename} ${imageDir}/roster_nolayout.txt  
        ./parseNamesStanford.py ${imageDir}/roster.txt ${imageDir}/roster_nolayout.txt ${imageDir}/
else     
        # parse the names (Tufts)
        # there may be some .ppm files, so we convert them to .jpg
        ppms=`ls ${imageDir}/*.ppm 2>/dev/null`
        for p in $ppms; do
                jpg_name=${p%.*}.jpg
                ../../../ImageMagick/bin/convert $p $jpg_name
                rm $p
        done
        ./parseNames.py ${imageDir}/roster.txt ${imageDir}
fi

