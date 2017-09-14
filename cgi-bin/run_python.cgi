#!/bin/bash

export PATH=/afs/cs.stanford.edu/u/cgregg/python_local/bin:$PATH
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/afs/cs.stanford.edu/u/cgregg/python_local/lib:/afs/cs.stanford.edu/u/cgregg/.local/lib:/afs/cs.stanford.edu/u/cgregg/.local/lib/libffi_lib64

#printf "Content-Type: text/html\n\n"

if [ -z ${QUERY_STRING} ]; then
        # no query string set, so just run everything passed into this script
        #echo 'No query string<p>'
        python $@
else
        # there is a query string
        #echo 'We have a query string.<p>'
        # find the script_to_run variable and run it
        saveIFS=$IFS
        IFS='=&'
        parm=($QUERY_STRING)
        IFS=$saveIFS
        declare -A array
        for ((i=0; i<${#parm[@]}; i+=2))
        do
                    array[${parm[i]}]=${parm[i+1]}
        done
        #echo ${array[script_to_run]}
        #echo "<p>"
        #echo `python ${array[script_to_run]} 2>&1`
        cd `dirname ${array[script_to_run]}`
        #printf "`basename ${array[script_to_run]}`" 
        python `basename ${array[script_to_run]}`
fi


