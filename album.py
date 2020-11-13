import re

CSV_CAN_HANDLE_UTF8 = False


def removeUTF8Char(string):
    if CSV_CAN_HANDLE_UTF8:
        return string
    else:
        return re.sub(r'[^\x00-\x7f]', r'', string)


class Album():
    attributeList = ['artist', 'title', 'rating', 'genre']

    def __init__(self, videoSnippet, playlistGenre):
        artist, title = '', ''
        artistAndAlbum = videoSnippet['title'].replace("ALBUM REVIEW", "").split('-')

        if len(artistAndAlbum) < 2:
            artistAndAlbum = videoSnippet['title'].replace("ALBUM REVIEW", "").split('|')
        try:
            # remove any unicode char from artist and title
            # so we can print the album in to a csv
            artist = removeUTF8Char(artistAndAlbum[0].strip())
            title = removeUTF8Char(artistAndAlbum[1].strip())
        except IndexError:
            artist = removeUTF8Char(artistAndAlbum[0].strip())
            title = removeUTF8Char(artistAndAlbum[0].strip())
            print('Error artist name and title are not parse-able:', artistAndAlbum)

        rating = []
        for line in videoSnippet['description'].split('\n'):
            if len(score := re.findall('.*/10', line)) > 0:
                rating = score

        if len(rating) > 0:
            rating = removeUTF8Char(rating[0])
        else:
            rating = 'NO SCORE'

        self.artist = artist
        self.title = title
        self.rating = rating
        self.genre = playlistGenre

        return

    def __str__(self):
        return \
            'Artist: ' + self.artist + \
            '\nTitle: ' + self.title + \
            '\nRating: ' + self.rating + \
            '\nGenre: ' + self.genre

    def getCsvRow(self):
        return self.__dict__
