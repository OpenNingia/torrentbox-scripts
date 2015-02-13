#!/usr/bin/python

import sys
from pushbullet import PushBullet

PB_API_KEY = ""

def __push_torrent_status(torname, torstatus, torlabel, torhash):
    pb = PushBullet(PB_API_KEY)

    success = False
    push = None
    if torstatus == '1':
        success, push = pb.push_note("Torrent in errore",
                                     """ \
Nome: {nm},
Label: {lb},
Info: {hh}
""".format(nm=torname, lb=torlabel, hh=torhash))


def push_torrent_status(torname, torstatus, torstatmsg, torlabel, torhash):

    if (    torstatus != '3' and
            torstatus != '13'):
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
    pb = PushBullet(PB_API_KEY)

    success, push = pb.push_note("Torrent completato",
                                 """ \
Nome: {nm},
Label: {lb},
Info: {hh}
""".format(nm=torname, lb=torlabel, hh=torhash))


def main():
    if len(sys.argv) < 1:
        return

    what = sys.argv[1]
    if what == 's':
        push_torrent_status(sys.argv[2], sys.argv[3], sys.argv[4],
                            sys.argv[5], sys.argv[6])
    else:
        push_torrent_finish(sys.argv[2], sys.argv[3], sys.argv[4])

if __name__ == '__main__':
    main()
