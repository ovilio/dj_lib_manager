import csv
import os
import argparse
import sys

from tinytag import TinyTag
import re


def main():
    args = setup_args()
    playlist_csv = args.file

    track_dic = _parse_dic_from_csv(playlist_csv)

    if args.format:
        _save_csv(track_dic)
        sys.exit()

    # get list of filenames in current directory
    files_list = filter(lambda x: x.endswith('.mp3') | x.endswith('.flac'), os.listdir())

    for fileName in files_list:
        # get metadata from each file
        file_metadata = TinyTag.get(fileName)
        title = _get_simple_title(file_metadata.title)
        print(f'Trying to found csv line by track title: "{title}"')
        found_track = track_dic.get(title)
        if found_track is not None:
            # mark track as downloaded and put into dictionary
            found_track.is_downloaded = True
            track_dic.update({found_track.title: found_track})
            print('found: ' + str(found_track))
        else:
            print(title + ' is not found')

    _save_csv(track_dic)
    sys.exit()


def _save_csv(track_dict):
    with open('new.csv', mode='w', encoding='utf-8') as result_csv:
        csv_writer = csv.writer(result_csv, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['Track name', 'Artist name', 'Album', 'Is downloaded', 'Cant download'])
        for track in track_dict.values():
            csv_writer.writerow([track.original_name, track.artist, track.album, track.is_downloaded])


def _parse_dic_from_csv(csv_filename) -> dict:
    dictionary = {}
    print('Starting parsing ' + csv_filename)
    with open(csv_filename, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # skip the header
        for csvLine in csv_reader:
            # fill dictionary of tracks with tracks from csv (key = trackname)
            title = _get_simple_title(csvLine[0])
            track = Track(csvLine[0], title, csvLine[1], csvLine[2])
            dictionary[track.title] = track
    print("Success!")
    return dictionary


def _get_simple_title(title) -> str:
    """This method exclude from track name text separated by '-' and '(' chars"""

    return re.split('\(|-', title, 1)[0].strip().lower()


class Track(object):
    """Class to store track data"""

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
        "-f",
        "--file",
        help="path to .csv file",
        type=str,
        default="123.csv",
        required=False
    )
    parser.add_argument(
        "--format",
        help="just format csv file and quit",
        action="store_true",
        default=False,
        required=False
    )
    return parser.parse_args()


if __name__ == '__main__':
    main()
