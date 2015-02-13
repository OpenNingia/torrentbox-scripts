#!/usr/bin/python
__author__ = 'Daniele Simonetti <oppifjellet@gmail.com>'

import logging
from pushbullet import PushBullet, Listener
from subprocess import call

logging.basicConfig(level=logging.DEBUG)

PB_API_KEY = ''  # YOUR API KEY
DEVICE_ID = ''  # id of device if None the listener listen all pushes
HTTP_PROXY_HOST = None
HTTP_PROXY_PORT = None

pb = PushBullet(PB_API_KEY)
ma = None


def on_push(psh):
    print ('received push:', psh)
    psh_type = psh['type']
    psh_subtype = psh['subtype'] if 'subtype' in psh else None

    print('type', psh_type, 'subtype', psh_subtype)

    if psh_type == 'tickle':
        on_tickle()
    elif psh_type == 'push':
        pass

def on_tickle():
    global ma

    print('get pushes', ma)
    success, pushes = pb.get_pushes(ma)
    if not success:
        return

    ma = pushes[0][u'modified']
    print('last modified', ma)

    for p in pushes:

        if 'source_device_iden' in p:
            print(p['source_device_iden'])
        if 'title' in p:
            print(p['title'])
        elif 'url' in p:
            print(p['url'])

        if 'url' in p:
            on_url(p['url'])


def on_url(url):
    if not 'torrent' in url:
        print('not a torrent')

    call(['wget', '-P', '/home/daniele/Scaricati/autotorrents/', '-O', '/home/daniele/Scaricati/autotorrents/tmp.torrent', url])

def main():
    global ma

    success, pushes = pb.get_pushes()
    if success:
        ma = pushes[0][u'modified']
        print('last modified', ma)

    s = Listener(pb,
                 on_push=on_push,
                 http_proxy_host=HTTP_PROXY_HOST,
                 http_proxy_port=HTTP_PROXY_PORT)
    try:
        s.run_forever()
    except KeyboardInterrupt:
        s.close()


if __name__ == '__main__':
    main()
