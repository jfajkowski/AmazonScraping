from bs4 import BeautifulSoup
import urllib2
import requests
import os
import time
from random import random
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from difflib import SequenceMatcher as SM

__author__ = "fajqa"
script_dir = os.path.abspath(__file__)

def prepare_song_set():
    unique_song_set = set()

    # Read from file
    with open(os.path.dirname(os.path.abspath(__file__)) + "/database/amazon_tracks.txt") as f_in:
        for line in f_in:
            unique_song_set.add(line.rstrip())

    # Split by separator
    unique_song_set = [unique_song.split('<SEP>') for unique_song in unique_song_set]

    # Construct search list
    for unique_song in unique_song_set:
        unique_song.append(
            'http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Ddigital-music&field-keywords=' +
            urllib2.quote(unique_song[2].replace(' ', '+') + '+' + unique_song[3].replace(' ', '+')))

    log("Ready to crawl...")
    return unique_song_set


def crawl(unique_song_set):
    log("Crawling started...")

    for unique_song in unique_song_set:
        try:
            search_and_download(unique_song)
            song_communicate("[SAVED]", unique_song)
        except AttributeError:
            song_communicate("[NOT FOUND]", unique_song)
        except (urllib2.HTTPError, urllib2.URLError) as e:
            print e
        except Exception as e:
            song_communicate("[ERROR] " + '[' + "%s" % e + ']', unique_song)
        finally:
            time.sleep(2+random())

    log("Crawling ended...")


def search_and_download(unique_song):
    response = requests.get(unique_song[4])
    soup = BeautifulSoup(response.text, "lxml")

    link = soup.find(id='result_0').contents[0].div.a.attrs['flashurl']

    response = urllib2.urlopen(link)
    track = response.read()

    create_directory(unique_song)

    with open(unique_song[0] + '.mp3', "wb") as f_out: f_out.write(track)

    check_mp3(unique_song, unique_song[0] + '.mp3')


def create_directory(unique_song):
    directory = os.path.dirname(script_dir) + "/songs/" + \
                unique_song[0][2] + "/" + \
                unique_song[0][3] + "/" + \
                unique_song[0][4] + "/"
    if not os.path.exists(directory):
        os.makedirs(directory)
    os.chdir(directory)


def check_mp3(unique_song, mp3_file):
    mp3 = MP3(mp3_file, ID3=EasyID3)
    duration = mp3.info.length

    real_title = mp3.tags['title'][0].lower()
    real_artist = mp3.tags['artist'][0].lower()

    wanted_title = unique_song[3].lower()
    wanted_artist = unique_song[2].lower()

    wanted_title = wanted_title.decode("UTF-8", errors="ignore")
    wanted_artist = wanted_artist.decode("UTF-8", errors="ignore")
    real_title = real_title.decode("UTF-8", errors="ignore")
    real_artist = real_artist.decode("UTF-8", errors="ignore")

    if not 25 < duration < 35:
        raise Exception("Duration: " + str(duration) + "s is not correct.")

    if not 0.75 < SM(None, wanted_artist, real_artist).ratio() <= 1:
        raise Exception("Artist: " + real_artist + " differs from: " + wanted_artist)

    if not 0.75 < SM(None, wanted_title, real_title).ratio() <= 1:
        raise Exception("Title: " + real_title + " differs from: " + wanted_title)


def log(text_line):
    print "[" + time.strftime("%X") + "] " + text_line


def song_communicate(communicate, unique_song):
    log(communicate + " " + unique_song[0] + " [ARTIST] " + unique_song[2] + " [TITLE] " + unique_song[3])


if __name__ == '__main__':
    unique_song_set = prepare_song_set()
    crawl(unique_song_set)
