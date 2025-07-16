#!/bin/sh

python3 -m venv geocat-venv
. geocat-venv/bin/activate
pip install requests python-dotenv dicttoxml lxml pyyaml
