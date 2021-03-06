#!/usr/bin/env python3
import argparse
import errno
import os
import re
import sys
from urllib.parse import urlparse


def generate_new_uri(params):
    """
    Generate new magnet uri from params dictionary
    :param params: list of trackers
    :return: a string in URI / Magnet format
    """
    uri = 'magnet:?'
    uri = uri + 'xt=' + params['xt'] + '&'
    for tr in params['tr']:
        uri = uri + 'tr=' + tr + '&'
    return uri[:-1]


if __name__ == '__main__':
    # Parse given args
    parser = argparse.ArgumentParser()
    parser.add_argument('--uri', '-u', dest='base_uri', help='The magnet uri to cleanup')
    parser.add_argument('--redirect-to', '-r', dest='redirect_to', nargs='?',
                        help='The program that will handle the cleaned URI')
    parser.add_argument('--max', dest='max_tracker', type=int, help='Set a max number of trackers')
    args = parser.parse_args()

    # Parse the given uri into an object
    parsed_base_uri = urlparse(args.base_uri)

    # Check if the given URI is a magnet link
    if parsed_base_uri.scheme == 'magnet':
        # Split the query on '&' in order to get the parameters list
        splitted_query = re.split('&', parsed_base_uri.query)

        trackers = []
        uri_params = {}
        bl_trackers = []
        bl_counter = 0
        tr_counter = 0

        # Load blacklisted trackers
        try:
            bl_file = open('blacklist.txt', 'r')
            for line in bl_file:
                bl_trackers.append(line.rstrip())
            bl_file.close()
        except FileNotFoundError:
            print('Blacklist file not found !')
            sys.exit(errno.ENOENT)

        # Iterate over parameters to found blacklisted trackers
        for param in splitted_query:
            splitted_param = re.split('=', param)

            # If the param begins with 'tr', it's a tracker
            if splitted_param[0] == 'tr':
                tracker = splitted_param[1]
                if tracker in bl_trackers:
                    bl_counter += 1
                else:
                    # if no max number of tracker defined add it
                    if args.max_tracker is None:
                        trackers.append(tracker)
                        tr_counter += 1
                    else:
                        # if the number of trackers < given max argument, add it
                        if tr_counter < args.max_tracker:
                            trackers.append(tracker)
                            tr_counter += 1
            else:
                # Just store the param to reuse it later
                uri_params[splitted_param[0]] = splitted_param[1]

        print(bl_counter, 'blacklisted trackers found !')
        print(tr_counter, 'tracker(s) left')
        if not trackers:
            print("All trackers from the magnet link were removed !")
        else:
            uri_params['tr'] = trackers
            new_uri = generate_new_uri(uri_params)

            if args.redirect_to is None:
                print(new_uri)
            else:
                command = args.redirect_to + " " + new_uri
                os.system(command)
    else:
        print('Sorry, this is not a magnet URI')

    sys.exit(0)
