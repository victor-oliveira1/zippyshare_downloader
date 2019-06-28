#!/bin/python3
#Copyright (C) 2018 Victor Oliveira <victor.oliveira@gmx.com>
#This work is free. You can redistribute it and/or modify it under the
#terms of the Do What The Fuck You Want To Public License, Version 2,
#as published by Sam Hocevar. See the COPYING file for more details.

from urllib import request
from urllib import parse
import argparse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

BUFFER = 1024 * 8

def Download(url, show_only=False, check=False):
    #Get the download URL using PhantomJS
    print('Processing URL:', url)
    driver.get(url)
    element = driver.find_element_by_id('dlbutton')
    url_download = element.get_attribute('href')

    if show_only:
        return url_download

    #Get filename from url_download
    filename = parse.unquote(url_download).split('/')[-1]

    #Starting download
    req = request.urlopen(url_download)
    filesize = req.length #Size in Bytes

    if check:
        return url_download, filename, filesize

    print('File:', filename)
    print('File size:', '{:.1f}MB'.format(filesize / 1000 / 1000))
    print('Starting download...')
    with open(filename, 'wb') as file:
        c = 0
        while True:
            tmp = req.read(BUFFER)
            if tmp:
                file.write(tmp)
                c += 1
                print('{:.1f}%'.format((c * BUFFER / filesize) * 100),
                      end='\r')
            else:
                break

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('url',
                        help='Zippyshare url to download file')
    parser.add_argument('-s',
                        help='show-only download URL',
                        action='store_true')
    parser.add_argument('-c',
                        help='show url_download, filename and filesize only',
                        action='store_true')
    args = parser.parse_args()

    if args.s:
        url_download = Download(args.url, show_only=True)
        print(url_download)

    elif args.c:
        url_download, filename, filesize = Download(args.url, check=True)
        print('URL_Download: {}\nFilename: {}\nFilesize: {:.1f}MB'.format(
            url_download,
            filename,
            filesize / 1000 / 1000))
    else:
        Download(args.url)
