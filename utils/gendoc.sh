#!/bin/bash

cd ../mahjong
for file in `ls | grep  '.py$' | sed s/.py//`
do
    python3 -m pydoc -w ./$file.py
    if [ $? = 0 ]
    then
        mv $file.html ../docs
    fi
done

