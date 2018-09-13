#!/bin/bash

export FLASK_APP=flsk-remote
export FLASK_DEBUG=false
pip3 install --upgrade --force-reinstall . --user
clear
flask run -h "0.0.0.0"
