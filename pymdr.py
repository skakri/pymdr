#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from pymdr import player

player = player.Player()
player.ui_create()
player.load_config()

if __name__ == "__main__":
    player.browser.run()
