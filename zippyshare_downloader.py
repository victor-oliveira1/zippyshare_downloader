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

def dl(url):
    if not 'zippyshare.com/v/' in url:
        print('Invalid URL')
        exit(1)

    print('Starting Zippyshare Downloader for %s...'%url)


    process = Popen(["phantomjs", "zippySolver.js", url], stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()

    print("output:"+output.decode('utf-8'))

    url_download = output.decode('utf-8').rstrip()

    filename_encoded = re.findall('"/.*"', output)[0].strip('"/')
    filename = parse.unquote(filename_encoded)

    req_download = request.urlopen(url_download)
    filesize = int(req_download.getheader('Content-Length'))
    print('Downloading: {}'.format(filename))
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

