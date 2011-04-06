#!/bin/bash

cd ../mahjong
find . -name "*.pyc" -exec rm {} \;
find . -name "*.py" -exec dos2unix {} \;

