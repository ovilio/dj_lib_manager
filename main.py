import csv
import os
import click
from Track import Track
from tinytag import TinyTag


def main():
    # open csv
    playlist_csv = './resources/playlist.csv'
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


if __name__ == '__main__':
    main()
