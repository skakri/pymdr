#PyMDr - python draugiem.lv/music player

##Setup
PyMDr depends on avbin and ffmpeg (check your package manager)

    virtualenv --python=/usr/bin/python2.7 --no-site-packages virtualenv
     . virtualenv/bin/activate
    pip install -r requirements.txt
    ./pymdr.py

##Features
* (probably) plays music from draugiem.lv
* caches files locally (mp3, artist_id-song_name_hash.mp3)

##Bugs and TODO
* get rid of sh/ffmpeg dependencies if possible (someone knows a good .flv library?)
* if not, implement queued fetching/encoding in background
* sane interface
* error caching, input validation
* pagination
* implement configuration (cache naming convention, cache folder, use subfolders, cache playlists, use clear interval?)
* code clean up (codged in few hours)
* check if runs on windows, if possible - package via pyinstaller/py2exe/?
* ??? and obligatory profit
