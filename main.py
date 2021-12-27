import csv
import os
# import click
import argparse
from tinytag import TinyTag
import re


def main():
    # open csv
    # playlist_csv = './resources/playlist.csv'

    playlist_csv = setup_args().f
    track_dic = parse_dic_from_csv(playlist_csv)

    # get list of filenames in current directory
    files_list = filter(lambda x: x.endswith('.mp3') | x.endswith('.flac'), os.listdir())

    for fileName in files_list:
        # get metadata from each file
        file_metadata = TinyTag.get(fileName)
        title = _get_simple_title(file_metadata.title)[0]
        print('Trying to found csv line by track title: ' + title)
        found_track = track_dic.get(title)
        if found_track is not None:
            print('found: ' + str(found_track))
            # mark track as downloaded and put into dictionary
            found_track.is_downloaded = True
            track_dic.update({found_track.title: found_track})
        else:
            print(title + ' is not found')

    save_csv(track_dic)


def save_csv(track_dic):
    with open('new.csv', mode='w', encoding='utf-8') as result_csv:
        csv_writer = csv.writer(result_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['Track name', 'Artist name', 'Album', 'is downloaded'])
        for track_row in track_dic.values():
            csv_writer.writerow([track_row.title, track_row.artist, track_row.album, track_row.is_downloaded])


def parse_dic_from_csv(playlist_csv):
    dictionary = {}
    print('Starting parsing ' + playlist_csv)
    with open(playlist_csv, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # to skip the header
        for csvLine in csv_reader:
            # fill dictionary of tracks with tracks from csv (key = trackname)
            temp = _get_simple_title(csvLine[0])
            track = Track(temp[0], csvLine[1], csvLine[2])
            # in a case when trackname contains additional info - add it
            if len(temp) > 1:
                track.info = temp[1]
            dictionary[track.title] = track
    print('List of tracks titles from csv')
    for elem in dictionary:
        print(elem)
    return dictionary


def _get_simple_title(title):
    return list(map(lambda x: x.strip().lower(), re.split('\(|-', title, 1)))


class Track(object):

    def __init__(self, title, artist, album, info='', is_downloaded=False):
        self.title = title
        self.info = info
        self.artist = artist
        self.album = album
        self.is_downloaded = is_downloaded

    def __str__(self):
        return f'{self.title} | {self.info} | {self.artist} | {self.album} | {str(self.is_downloaded)}'


def setup_args():
    parser = argparse.ArgumentParser(
        description='A tutorial of argparse!',
        epilog='',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--f",
        help="path to csv",
        type=str,
        required=True
    )
    parser.add_argument(
        "--h",
        default=1,
        help="show this help message and exit")
    return parser.parse_args()


if __name__ == '__main__':
    main()
