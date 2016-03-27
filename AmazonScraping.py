from bs4 import BeautifulSoup
import logging
import urllib2
import os
import requests
import random
import time
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from difflib import SequenceMatcher as SM

__author__ = "fajqa"


def prepare_logger():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %H:%M:%S',
                        filename=os.path.dirname(os.path.abspath(__file__)) + "/log/AmazonScraping.log",
                        filemode='w')
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # disable requests INFO messages
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    # set a format which is simpler for console use
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)


def prepare_song_set():
    unique_song_set = set()

    # Read from file
    with open(os.path.dirname(os.path.abspath(__file__)) + "/database/amazon_tracks.txt") as f_in:
        for line in f_in:
                unique_song_set.add(line.rstrip())

    # Split by separator
    unique_song_set = [us.split('<SEP>') for us in unique_song_set]

    # Construct search list
    for us in unique_song_set:
        us.append(
            'http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Ddigital-music&field-keywords=' +
            us[2].replace(' ', '+') + '+' + us[3].replace(' ', '+'))

    logging.info("Ready to crawl...")
    return unique_song_set


def create_directory(us):
    directory = "/home/fajqa/Documents/Python/AmazonScraping/songs/" + us[0][2] + "/" + us[0][3] + "/" + us[0][4] + "/"
    if not os.path.exists(directory):
        os.makedirs(directory)
    os.chdir(directory)


def check_mp3(us, mp3_file):
    mp3 = MP3(mp3_file, ID3=EasyID3)
    duration = mp3.info.length
    title = mp3.tags['title'][0]

    if not 25 < duration < 35:
        raise Exception("Duration: " + str(duration) + "s is not correct.")

    if not 0.1 < SM(None, us[3], title).ratio() <= 1:
        raise Exception("Title: " + title + " differs from: " + us[3])


def search_and_download(us):
    response = requests.get(us[4])
    soup = BeautifulSoup(response.text, "lxml")

    try:
        link = soup.find(id='result_0').contents[0].div.a.attrs['flashurl']
        response = urllib2.urlopen(link)
        track = response.read()

        create_directory(us)

        with open(us[0] + '.mp3', "wb") as f_out: f_out.write(track)

        check_mp3(us, us[0] + '.mp3')

        logging.info('[File] ID: ' + us[0] + " - SAVED")
    except AttributeError:
        logging.warning('[File] ID: ' + us[0] + " - NOT FOUND")
    except Exception as e:
        logging.warning("[File] ID: " + us[0] + " - ERROR: " + e.message)


def crawl(unique_song_set):
    logging.info("Crawling started...")

    for us in unique_song_set:
        search_and_download(us)
        time.sleep(0.5)

    logging.info("Crawling ended...")

if __name__ == '__main__':
    prepare_logger()
    unique_song_set = prepare_song_set()
    crawl(unique_song_set)