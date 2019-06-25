#!/bin/bash
multitime -n 500 grep "facebook" /mnt/hgfs/Logs/* > greptrash
multitime -q -n 500 ~/PycharmProjects/logParser/parser.py -f -l=/mnt/hgfs/Logs -k facebook -s test
