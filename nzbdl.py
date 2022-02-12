#!/usr/bin/env python3
from xmltodict import parse
from nntpdl import get_file

def get_files(nzb_dict):
    out = {}
    for f in nzb_dict["nzb"]["file"]:
        fn = f["@subject"].split('"')[1]

        if type(f["segments"]["segment"]) is not list:
            segments = [f["segments"]["segment"]["#text"]]
            sizes = [f["segments"]["segment"]["@bytes"]]
        else:
            segments = []
            sizes = []
            for segment in f["segments"]["segment"]:
                segments.append(segment["#text"])
                sizes.append(int(segment["@bytes"]))

        if type(f["groups"]["group"]) is not list:
            out[fn] = (f["groups"]["group"], segments, sizes)
        else:
            out[fn] = ( [g["#text"] for g in f["groups"]["group"]], segments, sizes)
    return out

def main():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("nzb")
    args = parser.parse_args()
    with open(args.nzb) as f:
        data = parse(f.read())
    files = get_files(data)
    for k,v in files.items():
        print(f"downloading {k}")
        get_file(v[1], group=v[0], filename=k, sizes=v[2])
    return 0

if __name__ == "__main__":
    from sys import exit
    exit(main())
