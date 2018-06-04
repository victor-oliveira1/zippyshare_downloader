#!/bin/python3
#Copyright (C) 2018 Victor Oliveira <victor.oliveira@gmx.com>
#This work is free. You can redistribute it and/or modify it under the
#terms of the Do What The Fuck You Want To Public License, Version 2,
#as published by Sam Hocevar. See the COPYING file for more details.

from urllib import request
from urllib import parse
import re
import os
import argparse
from subprocess import Popen, PIPE

BUFFER = 1024 * 8
BINPATH = os.path.dirname(os.path.realpath(__file__))

def dl(url):
    if not 'zippyshare.com/v/' in url:
        print('Invalid URL')
        exit(1)

    print('Starting Zippyshare Downloader for %s...'%url)

    # Call to the translation script
    if os.name == 'nt':
        process = Popen(["phantomjs.exe", os.path.join(BINPATH, "zippySolver.js"), url], stdout=PIPE)
    else:
        process = Popen(["phantomjs", os.path.join(BINPATH, "zippySolver.js"), url], stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()
    if exit_code!=0:
        print("Unable to transform the zippy link")
        return;

    # Transform the result
    url_download = output.decode('utf-8').rstrip()
    filename_encoded = url_download.rsplit('/', 1)[-1]
    filename = parse.unquote(filename_encoded)

    # Start the download
    req_download = request.urlopen(url_download)
    filesize = int(req_download.getheader('Content-Length'))
    print('Final link: {}'.format(url_download))
    print('File: {}'.format(filename))
    print('Size: {:.2f}MB'.format(filesize / 1000 / 1000))

    with open(filename, 'wb') as file:
        c = 0
        while True:
            tmp = req_download.read(BUFFER)
            if tmp:
                file.write(tmp)
                c += 1
                print('{:.1f}%'.format((c * BUFFER / filesize) * 100), end='\r')
            else:
                break

if __name__ == "__main__":
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('url',
                             help='URL or file with URLs to download')
    args = args_parser.parse_args()
    url = args.url

    if os.path.isfile(url):
        with open(url) as fp:
            for line in fp:
                dl(line.rstrip())
    else:
        dl(url)

