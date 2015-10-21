#!/usr/bin/python
import os
import sys
from subprocess import Popen, PIPE
def get_subtitles_track(file_path):

    sout, serr = Popen(['sh', 'FindSubtitleTrack.sh', file_path], stdout=PIPE, stderr=PIPE).communicate()
    # print(serr)
    return sout.strip()

def extract_srt(file_path):

    print('processing {}'.format(os.path.basename(file_path)))
    
    ass_path = os.path.splitext(file_path) [0] + ".ass"
    srt_path = os.path.splitext(file_path) [0] + ".srt"

    if os.path.exists(srt_path):
        print('> srt already exists')
        return

    if not os.path.exists(ass_path):
        extract_ass(file_path, ass_path)

    if os.path.exists(ass_path):
        convert_ass_to_srt(ass_path, srt_path)
        try:
            os.remove(ass_path)
        except:
            pass
    	print('> srt extraction OK')
    
def extract_ass(file_path, ass_path):

    # print('extracting ASS/SSA subtitles')

    trackns = get_subtitles_track(file_path)
    if trackns == None or trackns == "":
        print('> no subtitles track found.')
        return
    track_list = trackns.split()

    for t in track_list:
        try:    
            trackn = int(t) - 1
        except:
            print('> subtitles tracks incorrect: {}'.format(trackn))
            return
    
        print('> extract subtitles from track {}'.format(trackn))
        sout, serr = Popen(['mkvextract', 'tracks', file_path, "{}:{}".format(trackn, ass_path)], stdout=PIPE, stderr=PIPE).communicate()
    
    # print(serr)

def convert_ass_to_srt(ass_path, srt_path):
    
    sout, serr = Popen(['perl', 'ass2srt.pl', ass_path], stdout=PIPE, stderr=PIPE).communicate()
    print(serr)

    tx = ''
    with open(srt_path, 'rt') as fb:
        tx = fb.read().replace('\n\n','\n').replace('\\N', '\n')

    with open(srt_path, 'wt') as fb:
        fb.write(tx)

def main():

    if len(sys.argv) < 2:
        return

    import glob
    target = sys.argv[1]

    i = 0

    if os.path.isdir(target):
        for i, f in enumerate( [ os.path.join(target,x) for x in os.listdir(target) if x.endswith('.mkv') ] ):
            extract_srt(f)
        print('processed {} file(s)'.format(i))
    else:
        extract_srt(target)


if __name__ == '__main__':

    main()

