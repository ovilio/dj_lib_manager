import csv
import os
# import click
import argparse
from Track import Track
from tinytag import TinyTag


def main():
    # open csv
    # playlist_csv = './resources/playlist.csv'

    playlist_csv = setup_args().f
    track_dic = parse_dic_from_csv(playlist_csv)

    # get list of filenames in current directory
    filesInDirList = filter(lambda x: x.endswith('.mp3') | x.endswith('.flac'), os.listdir())

    for fileName in filesInDirList:
        # get metadata from each file
        fileMetaData = TinyTag.get(fileName)
        print('Trying to found csv line by track title: ' + fileMetaData.title.split()[0])
        foundTrack = track_dic.get(fileMetaData.title.split()[0])
        if foundTrack is not None:
            print('found: ' + str(foundTrack))
            # mark track as downloaded and put into dictionary
            foundTrack.is_downloaded = True
            track_dic.update({foundTrack.title: foundTrack})
        else:
            print(str(foundTrack) + ' is not found')

    print('List of tracks titles from csv')
    for elem in track_dic.values():
        print(elem)


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


def parse_dic_from_csv(playlist_csv):
    dictionary = {}
    print('Starting parsing ' + playlist_csv)
    with open(playlist_csv) as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # to skip the header
        for csvLine in csv_reader:
            # fill dictionary of tracks with tracks from csv (key = trackname)
            track = Track(csvLine[0], csvLine[1], csvLine[2])
            dictionary[track.title] = track
    print('List of tracks titles from csv')
    for elem in dictionary:
        print(elem)
    return dictionary


class Track(object):

    def __init__(self, name, artist, album, is_downloaded=False):
        temp = name.split("-")
        self.title = temp[0].strip()
        if len(temp) > 1:
            self.info = temp[1].strip()
        else:
            self.info = ''
        self.artist = artist
        self.album = album
        self.is_downloaded = is_downloaded

    def __str__(self):
        return self.title + ' | ' + self.info + ' | ' + self.artist + ' | ' + self.album + ' | ' + str(
            self.is_downloaded)


if __name__ == '__main__':
    main()
