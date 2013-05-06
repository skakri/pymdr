# -*- coding: utf-8 -*-

import os
import re
import urllib
from bs4 import BeautifulSoup


class Browser:
    def __init__(self, player):
        self.player = player
        self.base_url = 'http://www.draugiem.lv/music/'
        self.current = {
            'genre': 0,
            'subgenre': 0,
            'artist': 0,
            'playlist': 0,
            'song': 0,
            'artist_name': '',
            'song_name': ''
        }

    def run(self):
        if not self.current['playlist']:
            self.genres()
        else:
            self.playlist(self.current['playlist'], int(self.current['song']) + 1)

    def get(self, url):
        page = urllib.urlopen(url).read()
        page = BeautifulSoup(page)
        page.prettify()
        return page

    def get_playlist(self, artist_id):
        page = urllib.urlopen(self.base_url + 'rq/get.php?mids=' + artist_id + '&task=get_songs').read()
        page = BeautifulSoup(page)
        page.prettify()
        return page

    def genres(self):
        os.system('clear')
        self.player.ui_update_status('fetching genres')
        page = self.get(self.base_url + '?t=2')
        self.player.ui_update_status('')
        genres = page.select('.filterSubCat a')
        i = 0

        for genre in genres:
            print u'' + str(i) + ' ' + genre.text
            i += 1

        genre_index = raw_input('select a genre (0-' + str(len(genres) - 1) + ')')
        genre_link = genres[int(genre_index)]
        self.genre(genre_link)

    def genre(self, genre_link):
        os.system('clear')
        self.player.ui_update_status('fetching subgenres')
        page = self.get(self.base_url + genre_link['href'])
        self.player.ui_update_status('')
        genres = page.select('.filterSubCat a')
        i = 0

        for genre in genres:
            # print genre['href']
            print u'' + str(i) + ' ' + genre.text
            i += 1

        genre_index = raw_input('select a subgenre (0-' + str(len(genres) - 1) + ')')
        genre_link = genres[int(genre_index)]
        self.genre_page(genre_link)

    def genre_page(self, genre_link):
        os.system('clear')
        self.player.ui_update_status('fetching artists')
        self.current['subgenre'] = genre_link
        page = self.get(self.base_url + genre_link['href'])
        self.player.ui_update_status('')
        artists_ids = page.select('.artist-list .profileSmallIcon')
        artists = page.select('.artist-list h3 a')
        i = 0

        for artist in artists:
            print u'' + str(i) + ' ' + artist.text
            i += 1

        artist_index = raw_input('select a artist (0-' + str(len(artists) - 1) + ')')

        artist_id = artists_ids[int(artist_index)]['style']
        artist_id = re.findall('(\d+)\.jpg', artist_id)

        self.current['artist_name'] = artists[int(artist_index)].text
        self.current['playlist'] = artist_id[0]
        self.playlist(artist_id[0])

    def playlist(self, artist_id, song_id=None):
        os.system('clear')
        self.player.ui_update_status('loading tracks')
        playlist = self.get_playlist(artist_id)
        self.player.ui_update_status('')
        songs = playlist.select('song')
        i = 0

        if len(songs) == 0:
            self.player.ui_update_status('no tracks, returning to subgenre')
            self.genre_page(self.current['subgenre'])

        if not song_id:
            for song in songs:
                print u'' + str(i) + ' ' + song['name']
                i += 1

            song_index = raw_input('select a song (0-' + str(len(songs) - 1) + ')')
        else:
            # todo: toggle for loop
            if song_id + 1 > len(songs):
                song_id = 0
            song_index = song_id
        self.current['song'] = song_index
        song_link = songs[int(song_index)]['url']
        self.current['song_name'] = songs[int(song_index)]['name']

        self.player.ui_update_status('fetching song...')
        urllib.urlretrieve(song_link, self.player.config['cache_dir'] + '/tmp.flv')
        self.player.run()
