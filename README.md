nzbdl
=====

A python CLI application for downloading the files referenced by an [NZB](https://en.wikipedia.org/wiki/NZB) file.

```bash
export NNTP_SERVER=news.example.com
export NNTP_USER=user
export NNTP_PASSWORD=password # if not set, is prompted at run time
pip3 install git+https://github.com/sabnzbd/sabyenc
python3 nzbdl.py "Big Buck Bunny.nzb"
# if articles were missing when attempting download:
cd dl; par2 repair *.par2
```
