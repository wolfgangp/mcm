#!/usr/bin/env python

#it has been so modified as to be able to parse
#the cast of the first result tmdb returns
#for your input search string. It then parses the director's name,
#and renames the files like this: "Moviename [1850 Director].avi"
#Disclaimer: "This product uses the TMDb API but is not endorsed or certified by TMDb."

import tmdb
import urllib2
#import urllib3
import pprint
import sys
import readline
#import unicodedata as ud
import os
#from subprocess import call
import subprocess

from tmdb import config

language = 'en'
ziel = '/media/1.5TB/films/'
#ziel = 'ziel/'
#read api_key (register at tmdb.org to get one) from file
in_file = open("/usr/games/api_key", "rt")
#in_file = open("/home/juzzuj/code/api_key", "rt")
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
    
#function gives live output when calling subliminal (thanks ifischer http://stackoverflow.com/users/319905/ifischer)
def execsub(cargs):
    command = cargs[0]
    args = cargs[1:]
    print(command)
    print(args)
    process = subprocess.Popen(command, args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # Poll process for new output until finished
    while True:
        nextline = process.stdout.readline()
        if nextline == '' and process.poll() != None:
            break
        sys.stdout.write(nextline)
        sys.stdout.flush()
    output = process.communicate()[0]
    exitCode = process.returncode

    if (exitCode == 0):
        return output
    else:
        print('*** Something went wrong. subliminal exit code not 0 ***')

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
      guess = guess[0:24].title()
raw = rlinput('Film name ==>',guess)
m_tosearch = raw.decode('utf-8')
#m_tosearch = ud.normalize('NFC', m_tosearch)
#m_tosearch = m_tosearch.encode

print('    '+mfile[0]+'  (will handle this file)')
#Search for movie titles containing "Alien"
#movies = tmdb.Movies("Bottle Rocket", limit=True)
movies = tmdb.Movies(m_tosearch, limit=True)
#for movie in movies.iter_results():
rated = movies.get_ordered_matches()
#rated is a list of tuples. first value is match percentage, second is JSON
for num in range(0,len(rated)):
    if rated[num][0] > 74:
        #result=(rated[num][0]+' '+rated[num][1]['title'])
        #print(result)
        print('[' + str(num+1) + '] ' + rated[num][1]['title'].ljust(30) + '  (' + rated[num][1]['original_title'].rjust(30) + ')' + rated[num][1]['release_date'][0:4].rjust(6) + str(rated[num][0]).rjust(5) +'%' )
#print(rated[0][1]['title'])
print('\nChoose film. Press number:')
fno = input()
fno -= 1
fid = rated[fno][1]['id']
uri = config['urls']['movie.casts'] % fid
#uri = 'https://api.themoviedb.org/3/movie/'+str(fid)+'/casts?api_key='+api_key
#print(uri)
tmdbCore = tmdb.Core()
casts = tmdbCore.getJSON(uri,language)
directors = []
for i in casts['crew']:
            if i["job"] == "Director":
                directors.append({"id":i["id"],"name":i["name"]})                
print('# of directors: %s') % len(directors)

#MODIFY FOLLOWING TO GET SPECIFIC INFO
# Pick the movie whose title is exactly "Alien"
# Create a Movie object, fetching details about it
#movie = tmdb.Movie(fid)
#langs = movie.get_spoken_languages()
#tag = movie.get_tagline()
#blurb = movie.get_overview()
#print(tag + "   " + blurb)
#ortit = movie.get_original_title()
#tit = movie.get_title()
#print("\n" + ortit + " /// " + tit)
#print("link: http://www.themoviedb.org/movie/"+str(movie.get_id()))
#year = movie.get_release_date()

ye = rated[fno][1]['release_date'][0:4]
dir = directors[0]['name'].split()
#print(dir)
non = len(dir)
ln = dir[(non-1)].lower()
#ln = ln.encode('ascii', 'ignore')
fn = dir[0].lower()
#fn = fn.encode('ascii', 'ignore')
Ln = dir[(non-1)]
#Ln = Ln.encode('ascii', 'ignore')
dirn = ln +' '+ fn
#print(type(dirn))
tit = rated[fno][1]['title']
ortit = rated[fno][1]['original_title']
sugfn = tit + " [" + ye + " " + Ln + "]"
ext = str(mfile[0])[-4:]
sugfnext = sugfn + ext
sugfn_ez = ortit + " [" + ye + " " + Ln + "]"
print("Suggested dirname:      " + dirn)
#print("Suggested filename:     " + sugfn)
print("Original title:         " + sugfn_ez)

#print('\nShould\n' + str(mfile[0]) + '\nbe renamed to\n' + sugfnext + '\n[y]es or [n]o?')
que='\nShould\n    {} \nbe renamed to\n    {} \n[y]es or [n]o?'.format(mfile[0], sugfnext)
print(que)
deci = raw_input('==>')
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
        try:
            subprocess.check_output('subliminal -l en \"'+sugfnext+'\"', stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError, e:
            print "*** Subliminal reports code {} and\n{} ***".format(e.returncode, e.output)
        cont = os.listdir(".")
        for filename in cont:
          if filename.endswith("srt") or filename.endswith("sub"):
           sfile.append(filename)
        if len(sfile) > 0:
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
else:
    print('*** Nothing done ***')
# Access the fetched information about the movie
# full_info(self,movie_id)
# or other methods...
# overview = movie.get_overview()
