import sys, os, hashlib, StringIO, bencode

def pieces_generator(info):
    """Yield pieces from download file(s)."""
    piece_length = info['piece length']
    if 'files' in info: # yield pieces from a multi-file torrent
        piece = ""
        for file_info in info['files']:
            path = os.sep.join([info['name']] + file_info['path'])
            print path
            sfile = open(path.decode('UTF-8'), "rb")
            while True:
                piece += sfile.read(piece_length-len(piece))
                if len(piece) != piece_length:
                    sfile.close()
                    break
                yield piece
                piece = ""
        if piece != "":
            yield piece
    else: # yield pieces from a single file torrent
        path = info['name']
        print path
        sfile = open(path.decode('UTF-8'), "rb")
        while True:
            piece = sfile.read(piece_length)
            if not piece:
                sfile.close()
                return
            yield piece

def corruption_failure():
    """Display error message and exit"""
    print("download corrupted")
    exit(1)

def main():
    # Open torrent file
    torrent_file = open(sys.argv[1], "rb")
    metainfo = bencode.bdecode(torrent_file.read())
    info = metainfo['info']
    pieces = StringIO.StringIO(info['pieces'])
    # Iterate through pieces
    for piece in pieces_generator(info):
        # Compare piece hash with expected hash
        piece_hash = hashlib.sha1(piece).digest()
        if (piece_hash != pieces.read(20)):
            corruption_failure()
    # ensure we've read all pieces 
    if pieces.read():
        corruption_failure()

if __name__ == "__main__":
    main()