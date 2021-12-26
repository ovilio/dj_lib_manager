import csv
import os
from Track import Track
from tinytag import TinyTag

tracksDic = {}

# open csv
with open('./resources/playlist.csv') as csv_file:
    csvReader = csv.reader(csv_file)
    next(csvReader)
    for csvLine in csvReader:
        # fill dictionary of tracks with tracks from csv (key = trackname)
        track = Track(csvLine[0], csvLine[1], csvLine[2])
        tracksDic[track.title] = track

print('List of tracks titles from csv')
for elem in tracksDic:
    print(elem)

# get list of filenames in current directory
filesInDirList = filter(lambda x: x.endswith('.mp3') | x.endswith('.flac'), os.listdir())

for fileName in filesInDirList:
    # get metadata from each file
    fileMetaData = TinyTag.get(fileName)
    print('Trying to found csv line by track title: ' + fileMetaData.title.split()[0])
    foundTrack = tracksDic.get(fileMetaData.title.split()[0])
    print('found: ' + str(foundTrack))
    if foundTrack is not None:
        # mark track as downloaded and put into dictionary
        foundTrack.is_downloaded = True
        tracksDic.update({foundTrack.title: foundTrack})

print('List of tracks titles from csv')
for elem in tracksDic.values():
    print(elem)