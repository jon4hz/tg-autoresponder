#!/bin/sh
for f in ./data/*.session; do
    if [ ! -f "$f" ]; then
        python generate_session.py
        echo "Generated session file!"
        echo "Please stop the container with ctrl+c and start it detached with 'sudo docker-compose up -d'"
        read -r -d '' _ </dev/tty
    fi
done
for f in ./data/*.session; do
    if [ -f "$f" ]; then
        python autoresponder.py
    fi
done