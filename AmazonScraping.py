from bs4 import BeautifulSoup
import logging
import urllib2
import os
import requests
import time

__author__ = "fajqa"

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                    filename=os.path.dirname(os.path.abspath(__file__)) + "/log/AmazonScraping.log")

unique_song_set = set()
with open(os.path.dirname(os.path.abspath(__file__)) + "/database/a.txt") as f_in:
    for line in f_in:
        unique_song_set.add(line.rstrip())

# Split by separator
unique_song_set = [us.split('<SEP>') for us in unique_song_set]

# Construct search list
for us in unique_song_set:
    us.append(
        'http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Ddigital-music&field-keywords=' +
        us[2].replace(' ', '+') + '+' + us[3].replace(' ', '+'))

download_links = []

logging.info("Crawling started...")

for us in unique_song_set:
    response = requests.get(us[4])
    soup = BeautifulSoup(response.text, "lxml")
    soup.find(name="tr", attrs="id")


# xpath = '//tr[@id="result_0"]/td[1]/div/a/@flashurl'

logging.info("Crawling ended...")

for us in unique_song_set:
    if len(us[5]) == 0:
        logging.info('File: ' + us[2] + ' - ' + us[3] + ": NOT FOUND")

    else:
        response = urllib2.urlopen(us[5][0])
        track = response.read()

        directory = "/home/fajqa/Documents/Python/AmazonScraping/songs/" + us[0][2] + "/" + us[0][3] + "/" + us[0][4] + "/"
        if not os.path.exists(directory):
            os.makedirs(directory)
        os.chdir(directory)

        with open(us[0] + '.mp3', "wb") as f_out: f_out.write(track)

        logging.info('File: ' + us[2] + ' - ' + us[3] + ": SAVED")