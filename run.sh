#!/bin/run.sh
# Quick way to run
comment=$1
echo Commit comment: \"$comment\"
# upload in this folder
pip install -r requirements.txt
python app.py