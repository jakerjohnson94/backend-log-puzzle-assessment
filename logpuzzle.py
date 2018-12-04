#!/usr/bin/env python2
"""
Logpuzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Google's Python Class
http://code.google.com/edu/languages/google-python-class/

"""

import os
import re
import sys
import urllib
import argparse
import re

index_template = '''
<html>
<body>
    <div>
    {}
    </div>
</body>
</html>
'''


def read_file(filename):
    with open(filename) as file:
        data = file.read()
    return data


def parse_sorting_key(pat, txt):
    """sorting key helper function. Return regex match if possible
     or the original value"""
    r = re.search(pat, txt)
    return r.group(1) if r else txt


def create_img_tags(dest_dir):
    """Create string of HTML img tags from images in destination directory"""
    tags = []
    for img in sorted(os.listdir(dest_dir)):
        if img.endswith('.jpg'):
            tag = '<img src="{}" style="float: left">'.format(img)
            tags.append(tag)
    return '\n    '.join(tags)


def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order."""
    url_regex = r"GET.(\S*puzzle\S*)"
    sorting_regex = r'puzzle/\S-\S*-(\S*)\.jpg'
    data = read_file(filename)
    urls = set(['http://code.google.com' +
                m for m in re.findall(url_regex, data)])
    return sorted(urls, key=lambda x: parse_sorting_key(sorting_regex, x))


def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """
    if dest_dir not in os.listdir('.'):
        os.mkdir('./'+dest_dir)

    for i, img in enumerate(img_urls):
        print('downloading... ' + img)
        padding = '00' if i < 10 else '0' if i < 100 else ''
        urllib.urlretrieve(
            img, filename='./{}/img{}{}.jpg'.format(dest_dir, padding, str(i)))
    print('All Files Downloaded.')

    img_tags = create_img_tags(dest_dir)

    with open(dest_dir+'/index.html', 'w') as f:
        f.write(index_template.format((img_tags)))
        print('Wrote index.html in ./{}'.format(dest_dir))


def create_parser():
    """Create an argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--todir',  help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parse args, scan for urls, get images from urls"""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
