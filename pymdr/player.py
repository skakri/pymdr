# -*- coding: utf-8 -*-

import os
import browser
import pyglet

import sh
import datetime

class Player:
    def __init__(self, config=None):
        self.config = {
            'cache_dir': 'cache'
        }
        self.browser = browser.Browser(self)
        self.ui_create()
        self.load_config(config)

    def load_config(self, config):
        pass
        # self.ui_update_status('loading config (not implemented)')

    def ui_create(self):
        from blessings import Terminal
        self.ui = Terminal()

    def ui_update_status(self, text):
        with self.ui.location(0, self.ui.height - 2):
            print ' ' * 40
        with self.ui.location(0, self.ui.height - 2):
            print text

    def ui_update_current_song(self, text):
        with self.ui.location(self.ui.width-len(text)-1, self.ui.height - 2):
            print text

    def ui_update_progress(self, progress):
        if progress is 0:
            pass

        with self.ui.location(0, self.ui.height - 3):
            width = self.ui.width / 3
            print '[{0}{1}]'.format('#' * int(width * progress), ' ' * int(width - (width * progress)))


    def on_eos(self):
        pass
        # if self.player.playing:
        #     print 'pause'
        # else:
        #     print 'play'

    def exit_callback(self, dt):
        self.player.stop()
        pyglet.clock.unschedule(self.timer_callback)
        pyglet.clock.unschedule(self.exit_callback)
        self.player._sources = []
        # todo: use self.player._sources correctly - queue playlist in sources
        self.ui_update_status('stopped')
        self.browser.run()

    def timer_callback(self, dt):
        self.ui_update_status(
            'playing ' + str(datetime.timedelta(seconds=round(self.player._get_time()))) + '/' +
            str(datetime.timedelta(seconds=round(self.player.source.duration)))
        )
        self.ui_update_current_song(self.browser.current['artist_name'] + ' - ' + self.browser.current['song_name'])
        self.ui_update_progress(float(self.player._get_time()) / float(self.player.source.duration))

    def run(self, file_id):
        # todo: reuse player instance (start in __init__), use queue and pyglet.media.Player()
        pyglet.app.exit()
        self.player = pyglet.media.ManagedSoundPlayer()
        self.player.push_handlers(self)
        # self.player.eos_action = self.player.EOS_PAUSE

        if not os.path.exists(file_id + '.mp3'):
            self.ui_update_status('converting to mp3')
            convert = sh.ffmpeg(
                '-i', file_id + '.flv',
                '-f', 'mp3', file_id + '.mp3',
                '-y')
            convert.wait()
            os.remove(file_id + '.flv')

        self.ui_update_status('loading mp3')
        self.source = pyglet.media.load(file_id + '.mp3')
        pyglet.clock.schedule_once(self.exit_callback, self.source.duration)
        pyglet.clock.schedule_interval_soft(self.timer_callback, 0.1)

        self.player.queue(self.source)
        self.ui_update_status('playing')

        self.player.play()
        pyglet.app.run()
        pyglet.app.exit()
