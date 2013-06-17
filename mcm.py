#!/usr/bin/env python

#this script uses a slightly modified tmdb.py

#it has been so modified as to be able to parse
#the cast of the first result tmdb returns
#for your input search string. It then parses the director's name,
#and renames the files like this: "Moviename [1850 Director].avi"
#Disclaimer: "This product uses the TMDb API but is not endorsed or certified by TMDb."


import tmdb
import urllib2
import pprint
import sys
import readline
#import unicodedata as ud
import os
#from subprocess import call
import subprocess

ziel = '/media/1.5TB/films/'
#ziel = 'ziel/'

#read api_key (register at tmdb.org to get one) from file
in_file = open("/usr/games/api_key.txt", "rt")
#in_file = open("/home/juzzuj/temp/tmdb/api_key.txt", "rt")
api_key = in_file.read()
in_file.close()
tmdb.configure(api_key)

#user input prompt, which is prefilled and editable
def rlinput(prompt, prefill=''):
   readline.set_startup_hook(lambda: readline.insert_text(prefill))
   try:
      return raw_input(prompt)
   finally:
      readline.set_startup_hook()

#reads 

#help(tmdb.Movie)
#tmdb.core.getJSON("http://httpbin.org/get?m=hello")["args"]["m"],"hello")
cont = os.listdir(".")
mfile = []
for filename in cont:
  if filename.endswith("mkv") or filename.endswith("avi") or filename.endswith("mp4"):
    mfile.append(filename)
    #print(filename)
    
if len(mfile) > 1:
    print('*** More than one film file present, suggestion is first ***')

if len(mfile) == 0:
    print('*** No film files found ***')

guess = ""
if len(mfile) > 0:
      guess = str(mfile[0])
      guess = guess[:-4]
      guess = guess.replace('.',' ')  
      guess = guess[0:30]
      
raw = rlinput('Film name: ',guess)
#raw = raw_input("Movie name: ")
m_tosearch = raw.decode('utf-8')

#m_tosearch = ud.normalize('NFC', m_tosearch)
#m_tosearch = m_tosearch.encode

# Search for movie titles containing "Alien"
#movies = tmdb.Movies("Bottle Rocket", limit=True)
movies = tmdb.Movies(m_tosearch, limit=True)
for movie in movies.iter_results():
#    #Pick the movie whose title is exactly "Alien"
    if movie["title"] == m_tosearch or movie["original_title"] == m_tosearch:
#        # Create a Movie object, fetching details about it
        movie = tmdb.Movie(movie["id"])
        #langs = movie.get_spoken_languages()
        #tag = movie.get_tagline()
        #blurp = movie.get_overview()
        #print(tag + "   " + blurp)
        ortit = movie.get_original_title()
        tit = movie.get_title()
        print("\n" + ortit + " /// " + tit)
        print("link: http://www.themoviedb.org/movie/"+str(movie.get_id()))
        year = movie.get_release_date()
        m_info = movie.get_cast()
        minfo = str(m_info)
        numofdirectors = minfo.count("name")
        print('# of directors: ' + str(numofdirectors))
        break
    
col = m_info[0]
dir = '%(name)s' % \
col
ds = dir.split()
ln = ds[1].lower()
fn = ds[0].lower()
Ln = ds[1]
dirn = str(ln +' '+ fn)
ye = year[0:4]
sugfn = ortit + " [" + ye + " " + Ln + "]"
ext = str(mfile[0])[-4:]
sugfnext = sugfn + ext
sugfn_ez = tit + " [" + ye + " " + Ln + "]"
print("Suggested dirname:      " + dirn)
print("Suggested filename:     " + sugfn)
print("Easier title:           " + sugfn_ez)

print('\nShould\n' + str(mfile[0]) + '\nbe renamed to\n' + sugfnext + '\n[y]es or [n]o?')
deci = raw_input()
deci = str(deci)
nosubs = ''
idx = ''

if deci == 'y':
    os.rename(str(mfile[0]), sugfnext)
    sfile = []
    for filename in cont:
       if filename.endswith("srt") or filename.endswith("sub"):
        sfile.append(filename)
    if len(sfile) == 0:
        print('*** Invoking subliminal ***')
        #call(["subliminal", "-l en", sugfnext])
        #proc = subprocess.Popen(["subliminal", "-l en", sugfnext], stdout=subprocess.PIPE, )
        #subout = subprocess.check_output(["subliminal", "-l en", sugfnext])
        #returncode = subprocess.call(command, stdout=open('/dev/null', 'w'), stderr=subprocess.STDOUT)
        subli = subprocess.Popen(["subliminal", "-l en", sugfnext], stdout=open('/dev/null', 'w'), stderr=subprocess.STDOUT)
        out, err = subli.communicate()
        if out != False:
            print out
        if err != False:
            print err
        cont = os.listdir(".")
        for filename in cont:
          if filename.endswith("srt") or filename.endswith("sub"):
           sfile.append(filename)
        if '.' in str(sfile):
           schnuller = 1
        else:
           nosubs = 'y'
    if nosubs != 'y':
       sext = str(sfile[0])[-4:]
       if sext == '.sub':
             idxfn = str(sfile[0][:-3]) + 'idx'
             if os.path.isfile(idxfn):
                os.rename(idxfn, sugfn + '.idx')
                idx = 'y'
       os.rename(str(sfile[0]), sugfn + sext)
       print('*** ' + str(sfile[0]) + ' > ' + sugfn + sext + ' (subs handled) ***')
    if os.path.isdir(ziel + dirn):
       schnuller = 1
    else:
       os.mkdir(ziel + dirn)
       print('*** Directory ' + ziel + dirn + ' created ***')     
    os.rename(sugfnext, ziel + dirn + '/' + sugfnext)
    print('*** Film file moved to ' + ziel + dirn + '/ ***')
    if nosubs != 'y':
       os.rename(sugfn + sext, ziel + dirn + '/' + sugfn + sext)
       if idx == 'y':
         os.rename(sugfn + '.idx', ziel + dirn + '/' + sugfn + '.idx')
       print('*** Subtitles moved as well ***')
    print('*** Contents of ' + ziel + dirn + '/ : ***')
    subprocess.call(["ls", "-alh", ziel + dirn])
 
# Access the fetched information about the movie
# full_info(self,movie_id)
# or other methods...
# overview = movie.get_overview()
