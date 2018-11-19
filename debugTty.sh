#!/bin/bash

baudrate='b9600'
debug='-v -D -d -d'

socat ${debug} PTY,link=./pty1,${baudrate},cfmakeraw GOPEN:/dev/ttyUSB0,${baudrate},cfmakeraw 2> ttyLogFile.txt

