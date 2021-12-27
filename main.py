import csv
import os
import argparse
from tinytag import TinyTag
import re


def main():
    playlist_csv = setup_args().f
    track_dic = parse_dic_from_csv(playlist_csv)

    # get list of filenames in current directory
    files_list = filter(lambda x: x.endswith('.mp3') | x.endswith('.flac'), os.listdir())

    for fileName in files_list:
        # get metadata from each file
        file_metadata = TinyTag.get(fileName)
        title = _get_simple_title(file_metadata.title)
        print(f'Trying to found csv line by track title: "{title}"')
        found_track = track_dic.get(title)
        if found_track is not None:
            print('found: ' + str(found_track))
            # mark track as downloaded and put into dictionary
            found_track.is_downloaded = True
            track_dic.update({found_track.title: found_track})
        else:
            print(title + ' is not found')

    save_csv(track_dic)


def save_csv(track_dict):
    with open('new.csv', mode='w', encoding='utf-8') as result_csv:
        csv_writer = csv.writer(result_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['Track name', 'Artist name', 'Album', 'is downloaded', 'cant download'])
        for track in track_dict.values():
            csv_writer.writerow([track.original_name, track.artist, track.album, track.is_downloaded])


def parse_dic_from_csv(playlist_csv):
    dictionary = {}
    print('Starting parsing ' + playlist_csv)
    with open(playlist_csv, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        for csvLine in csv_reader:
            # fill dictionary of tracks with tracks from csv (key = trackname)
            title = _get_simple_title(csvLine[0])
            track = Track(csvLine[0], title, csvLine[1], csvLine[2])
            dictionary[track.title] = track
    print("Success!")
    return dictionary


def _get_simple_title(title):
    return re.split('\(|-', title, 1)[0].strip().lower()


class Track(object):

    def __init__(self, original_name, title, artist, album, is_downloaded=False):
        self.original_name = original_name
        self.title = title
        self.artist = artist
        self.album = album
        self.is_downloaded = is_downloaded

    def __str__(self):
        return f'{self.original_name} | {self.artist} | {self.album} | {str(self.is_downloaded)}'


def setup_args():
    parser = argparse.ArgumentParser(
        description='Music library management tool',
        epilog='',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--f",
        help="path to .csv file",
        type=str,
        default="123.csv",
        required=False
    )
    return parser.parse_args()


if __name__ == '__main__':
    main()
