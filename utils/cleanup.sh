#!/bin/bash

cd ../mahjong
find . -name "*.pyc" -exec rm -v {} \;
find . -name "*.py" -exec dos2unix {} \;

