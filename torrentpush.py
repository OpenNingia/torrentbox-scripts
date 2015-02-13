#!/usr/bin/python
__author__ = 'Daniele Simonetti <oppifjellet@gmail.com>'

import os
import sys
import json
from pushbullet import PushBullet

CFG_FILE = "torrentpush.conf"
PB_API_KEY = ""

class PushConfig(object):
    def __init__(self):

        self.push_on_status_changes = False
        self.push_on_completed = True
        self.statuses_to_push = []

        if os.path.exists(CFG_FILE):
            with open(CFG_FILE, 'rt') as fp:
                try:
                    js = json.load(fp)
                    if 'push_on_status_changes' in js:
                        self.push_on_status_changes = js['push_on_status_changes']
                    if 'push_on_completed' in js:
                        self.push_on_completed = js['push_on_completed']
                    if 'statuses_to_push' in js:
                        self.statuses_to_push = js['statuses_to_push']
                except:
                    pass

CFG_OBJ = PushConfig()

def push_torrent_status(torname, torstatus, torstatmsg, torlabel, torhash):

    if not CFG_OBJ.push_on_status_changes:
        return

    if torstatus not in CFG_OBJ.statuses_to_push:
        return

    pb = PushBullet(PB_API_KEY)

    success = False
    push = None
    success, push = pb.push_note("Torrent in status: {}".format(torstatmsg),
                                 """ \
Nome: {nm},
Label: {lb},
Info: {hh}
""".format(nm=torname, lb=torlabel, hh=torhash))


def push_torrent_finish(torname, torlabel, torhash):

    if not CFG_OBJ.push_on_completed:
        return

    pb = PushBullet(PB_API_KEY)

    success, push = pb.push_note("Torrent completato",
                                 """ \
Nome: {nm},
Label: {lb},
Info: {hh}
""".format(nm=torname, lb=torlabel, hh=torhash))


def main():
    if len(sys.argv) < 5:
        print('missing arguments')
        return
    try:
        what = sys.argv[1]
        if what == 's':
            push_torrent_status(sys.argv[2], sys.argv[3], sys.argv[4],
                                sys.argv[5], sys.argv[6])
        else:
            push_torrent_finish(sys.argv[2], sys.argv[3], sys.argv[4])
    except:
        print('push failed')

if __name__ == '__main__':
    main()
