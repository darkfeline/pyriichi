#!/bin/bash

cd mahjong
for file in `ls | grep  '.py$' | sed s/.py//`
do
    pydoc3 -w ./$file.py
    if [ $? = 0 ]
    then
        mv $file.html ../
    fi
done

