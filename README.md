mcm
===

mcm = movie collection mover
python movie file-handling script to parse movie files and rename and move files (tmdb.py library used to parse and subliminal to get subtitles)

files:

mcm.py

(tmdb.py and subliminal are required. see: https://github.com/doganaydin/themoviedb and https://github.com/Diaoul/subliminal , as well as their respective requirements.)

the script presupposes that current directory contains one movie file on which its guess at the title (no multi-volume support yet) is based. There is a prompt for you to submit an exact title. tmdb.org is then parsed for title, original title, year and director. A file naming scheme is then enforced:

%OriginalTitle [%Year %Director].%ext

%ext will be source movie file extension (.mkv/.avi/.mp4) as well as subtitle file extension .srt/.sub/.idx. If one subtitle file is found it's renamed accordingly. Else subliminal will be invoked to download English subtitles.

In a target directory you specify a folder will be created named

%director's last name %director's first name (example: 'kubrick stanley')

Both movie and subtitle files (including .idx if there) will then be moved.

It is all very simple and serves only highly specific needs. I'm a Python beginner. If you wanna drop me a line, please do.

-wolfgangp juzzuj@gmx.at
