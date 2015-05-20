#!/usr/bin/python
import glob
import os
import re

video = glob.glob("*.avi") + glob.glob("*.mkv") + glob.glob("*.mp4")
srt = glob.glob("*.srt")

def nu(s):
	m = re.search("0*(\d+)[eExX]0*(\d+)", s)
	#print m.group(1), m.group(2)
	return m.group(1, 2)

def sq(s):
	return "'" + s.replace("'", "'\\''") + "'"

vk = dict((nu(v), v) for v in video)
for s in srt:
	k = nu(s)
	if k not in vk: continue
	v = vk[k]
	t = os.path.splitext(v)[0] + ".srt"
	if s == t: print "#", s
	else: print "mv -i %s %s" % (sq(s), sq(t))
