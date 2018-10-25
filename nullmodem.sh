#!/bin/bash

baudrate='b9600'
debug='-v -D -d -d'

socat ${debug}                        \
PTY,link=./pty1,${baudrate},cfmakeraw \
PTY,link=./pty2,${baudrate},cfmakeraw 2> socatLogFile.txt

