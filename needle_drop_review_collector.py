import csv
from googleapiclient.discovery import build

from album import Album


CVS_FILE_NAME = 'albums_list.csv'


class NeedleDropReviewCollector:

    PLAY_LISTS_IDS = {
        # Key:Name of play list on YouTube
        # Value:Play list YouTube ID
        'Rock Reviews': 'PLP4CSgl7K7ori6-Iz-AWcX561iWCfapt_',

        'Hip Hop Reviews': 'PLP4CSgl7K7ormBIO138tYonB949PHnNcP',

        'Pop Reviews': 'PLP4CSgl7K7oqibt_5oDPppWxQ0iaxyyeq',

        'Electronic Reviews': 'PLP4CSgl7K7ormX2pL9h0inES2Ub630NoL',

        'Loud Rock Reviews: Metal, '
        'Hardcore Punk Variants, Extreme '
        'Shit': 'PLP4CSgl7K7orAG2zKtoJKnTt_bAnLwTXo',

        'Other Reviews: Singer-'
        'songwriters, Folk, Experimental,'
        ' Jazz, Oddballs, Misc.': 'PLP4CSgl7K7orSnEBkcBRqI5fDgKSs5c8o',

        'Classics': 'PLP4CSgl7K7or_7JI7RsEsptyS4wfLFGIN'
    }

    def __init__(self, apiKey):
        self.youtube = build('youtube', 'v3', developerKey=apiKey)
        self.allReveiwedAlbums = []
        return

    def run(self):
        self.startScraping()
        self.writeAlbumsToCsv()
        return

    def startScraping(self):
        print('Scrapping all of The Needle Drops Play List Album Scores!')
        for genre, playListId in NeedleDropReviewCollector.PLAY_LISTS_IDS.items():
            # This loop is to request each page of the play list
            print('Scrapping:', genre)

            nextPageToken = ""
            response = self.youtube.playlistItems().list(
                part="id",
                playlistId=playListId
            ).execute()

            pageInfo = response['pageInfo']
            totalPages = int(pageInfo['totalResults'] / pageInfo['resultsPerPage'])
            for _ in range(totalPages):
                try:
                    response = self.youtube.playlistItems().list(
                        part="id,snippet",
                        pageToken=nextPageToken,
                        playlistId=playListId
                    ).execute()

                    # build album list
                    self.buildAlbumList(response=response, playlistGenre=genre)

                    # get next page of albums
                    nextPageToken = response['nextPageToken']
                except KeyError as err:
                    # this means we ran out of pages
                    print("KeyError error: {0}".format(err))
                    # print(nextPageToken)
                    break
        return

    def buildAlbumList(self, response, playlistGenre):
        for item in response['items']:
            snippet = item['snippet']
            if 'ALBUM REVIEW' in snippet['title'].upper():
                self.allReveiwedAlbums.append(
                    Album(videoSnippet=snippet, playlistGenre=playlistGenre))
        return

    def writeAlbumsToCsv(self):
        if len(self.allReveiwedAlbums) <= 0:
            return

        with open(CVS_FILE_NAME, 'w', newline='') as csvfile:
            fieldnames = Album.attributeList
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for album in self.allReveiwedAlbums:
                try:
                    writer.writerow(album.getCsvRow())
                except UnicodeEncodeError as err:
                    print('ERROR in writeAlbumsToCsv: ', err, album.getCsvRow())
        return
