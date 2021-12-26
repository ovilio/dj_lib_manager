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
        return self.title + ' | ' + self.info + ' | ' + self.artist + ' | ' + self.album + ' | ' + str(self.is_downloaded)
