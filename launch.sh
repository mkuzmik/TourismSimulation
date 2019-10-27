#!/bin/bash

pip install -r requirements.txt
PYTHONPATH="`pwd`/src:`pwd`" python3 app/main.py