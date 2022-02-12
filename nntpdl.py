#!/usr/bin/env python3
from nntplib import NNTPPermanentError, NNTPTemporaryError
from nntplib import NNTP_SSL as NNTP
import sabyenc3
from re import search
import os.path
from os import environ
from getpass import getpass
from sys import stderr

server = environ.get("NNTP_SERVER", "localhost")
user = environ.get("NNTP_USER", "user")
password = environ.get("NNTP_PASSWORD", None)
if not password:
    password = getpass()
N = NNTP(server, user=user, password=password)
lastgroup = None
dest = environ.get("NNTP_DEST", "./dl")

def debug(text):
    print(text, file=stderr)

def set_group(group):
    global lastgroup
    if lastgroup != group:
        lastgroup = group
        return N.group(group)

def get_part(message_id, group=None):
    global N
    if group:
        set_group(group)
    try:
        resp, info = N.article(f"<{message_id}>")
    except NNTPTemporaryError:
        raise
    lines = info.lines[info.lines.index(b'')+1:]
    size = search('size=(.\d+?) ', lines[-1].decode("utf-8"))
    if size:
        size = int(size.group(1))
    else:
        raise Exception(f"Can't find size in {lines[-1].decode('utf-8')}")
    decoded_data, output_filename, crc, crc_yenc, crc_correct = sabyenc3.decode_usenet_chunks(lines,size)
    return decoded_data

def get_file(message_ids, group=None, filename=None, sizes=None):
    f = b''
    for n,m in enumerate(message_ids):
        debug(f"downloading {n+1} of {len(message_ids)}")
        try:
            f += get_part(m, group=group)
        except NNTPTemporaryError:
            debug(f"Couldn't get that article, adding 0x00 * {str(sizes[n])}")
            f += b"\0" * sizes[n]
            continue
    if filename:
        with open(os.path.join(dest, filename), "wb") as fh:
            fh.write(f)
    else:
        return f

def main():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("group")
    parser.add_argument("message", nargs="+")
    parser.add_argument("--filename")
    args = parser.parse_args()
    if not args.filename:
        print(get_file(args.message, group=args.group))
    else:
        get_file(args.message, group=args.group, filename=args.filename)
    return 0

if __name__ == "__main__":
    from sys import exit
    exit(main())
