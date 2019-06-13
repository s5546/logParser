#!/bin/bash
multitime -q -n 1250 ../logParser.bak.py -l=../../../syslogs -k facebook
multitime -n 1250 grep "facebook" ../../../syslogs/* > greptrash
