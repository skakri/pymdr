#PyMDr - python draugiem.lv/music player

##Setup
PyMDr depends on portaudio and ffmpeg (check your package manager)

    virtualenv --python=/usr/bin/python2.7 --no-site-packages virtualenv
     . virtualenv/bin/activate
    pip install -r requirements.txt
    ./pymdr.py

##Features
* (probably) plays music from draugiem.lv

##Bugs and TODO
* get rid of sh/ffmpeg dependencies if possible (someone knows a good .flv library?)
* if not, implement queued fetching/encoding in background
* sane interface
* error caching, input validation
* pagination
* implement configuration (save downloaded flv or encoded wav files or reencode to mp3s?)
* code clean up (codged in few hours)
* ??? and obligatory profit
