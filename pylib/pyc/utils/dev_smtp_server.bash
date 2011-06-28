#!/bin/bash

echo "Starting smtp server on localhost port 25"


sudo    \
    python -m smtpd -n -c DebuggingServer localhost:25