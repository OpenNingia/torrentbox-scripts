#!/bin/sh

export LC_ALL=C
mkvinfo "$1" | grep -B 2 "Track type: subtitles" | grep "Track number:" | awk "{{print \$5}}"
#echo `mkvinfo "$1"| grep 'Track type:'`