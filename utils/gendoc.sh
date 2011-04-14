#!/bin/bash

cd ../mahjong
for file in `ls | grep  '.py$' | sed s/.py//`
do
    python3 -m pydoc -w ./$file.py
    if [ $? = 0 ]
    then
        mv -v $file.html ../docs
    fi
done

for dir in `ls`
do
    if [ -d $dir ]
    then
        python3 -m pydoc -w $dir
        if [ $? = 0 ]
        then
            mv -v $dir.html ../docs
        fi
    fi
done
