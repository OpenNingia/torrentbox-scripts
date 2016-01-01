#!/usr/bin/python

from subprocess import call
import sys
import os

def download_subtitle(file_path):
    fname, fext = os.path.splitext(file_path)
    if fext not in [".mkv", ".avi", ".mp4"]:
        return False

    srt_name = "{}.ita.srt".format(fname)

    if os.path.exists(srt_name):
        print('SKIP {}'.format(file_path))
        return True

    with open('/dev/null', 'w') as devnull:
        if call(['python', 'OpenSubtitlesDownload.py', '-l', 'ita', file_path], stdout=devnull) == 0:
            print('DOWNLOADED {}'.format(srt_name))
            return True
        else:
            print('FAIL {}'.format(file_path))
            return False

def main():

    if len(sys.argv) < 2:
        return

    import glob
    target = sys.argv[1]

    if os.path.isdir(target):
        for i, f in enumerate( [ os.path.join(target,x) for x in os.listdir(target) ] ):
            download_subtitle(f)
    else:
        download_subtitle(target)


if __name__ == '__main__':
    main()
