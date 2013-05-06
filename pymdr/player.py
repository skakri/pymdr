# -*- coding: utf-8 -*-

import browser
import pyaudio
import wave
import sh
import datetime
from time import sleep
from ctypes import *

# From alsa-lib Git 3fd4ab9be0db7c7430ebd258f2717a976381715d
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)


def py_error_handler(*arg):
    # eh.
    pass

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

asound = cdll.LoadLibrary('libasound.so')

# Set error handler
asound.snd_lib_error_set_handler(c_error_handler)

# todo: move to config
CHUNK = 1024


class Player:
    def __init__(self):
        self.config = {
            'cache_dir': 'cache'
        }
        self.browser = browser.Browser(self)

    def load_config(self):
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

    def run(self):

        p = pyaudio.PyAudio()
        self.time = 0

        self.ui_update_status('converting to wav')
        convert = sh.ffmpeg(
            '-i', self.config['cache_dir'] + '/tmp.flv',
            '-f', 'wav', self.config['cache_dir'] + '/tmp',
            '-y')
        convert.wait()
        self.ui_update_status('loading wav')
        wf = wave.open(self.config['cache_dir'] + '/tmp', 'rb')

        def callback(in_data, frame_count, time_info, status):
            data = wf.readframes(frame_count)
            return (data, pyaudio.paContinue)

        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True,
                        stream_callback=callback)

        self.ui_update_status('playing')
        stream.start_stream()

        while stream.is_active():
            self.ui_update_status('playing ' + str(datetime.timedelta(seconds=round(self.time))))
            self.ui_update_current_song(self.browser.current['artist_name'] + ' - ' + self.browser.current['song_name'])
            sleep(0.1)
            self.time += 0.1

        stream.stop_stream()
        self.ui_update_status('stopped')
        stream.close()
        wf.close()

        p.terminate()
        self.browser.run()
