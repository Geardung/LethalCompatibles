@echo off
git clone https://github.com/Geardung/LethalCompatibles
cd LethalCompatibles
git config --global --add safe.directory .
py -m pip install --upgrade pip
py -m pip install -r reqs.txt
start start.bat