#!/bin/bash

if [[ -f $1 ]]; then
  mogrify -blur 0x10 -quality 50 -verbose $1
else
  echo 'No input files defined.'
fi
