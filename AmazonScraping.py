import scrapy
from scrapy.crawler import CrawlerProcess
import urllib2
import os
import time

__author__ = "fajqa"

def writeLog(msg):
    with open(os.path.dirname(os.path.abspath(__file__)) + "/log/AmazonScraping.log", "a") as f:
        text = time.strftime("[%d.%m.%Y  - %X] ") + msg
        f.write(text + "\n")
        print text

def parseByPath(path):
    # Open files and parse text
    list = []
    writeLog("Opening file: " + path + "...")
    with open(path, "r") as f_in: list = f_in.read()
    writeLog("Parsing " + path + "...")
    list = list.split('\n')[:-1]
    return list

unique_song_set = set(parseByPath(os.path.dirname(os.path.abspath(__file__)) + "/database/unique_tracks.txt"))
repeating_song_set = set(parseByPath(os.path.dirname(os.path.abspath(__file__)) + "/database/msd_acquired.txt"))

# Check for repetitions
writeLog("Deleting repeating songs...")
for rs in repeating_song_set:
    unique_song_set = [us for us in unique_song_set if not rs in us[0:17]]
    writeLog(rs)

for us in unique_song_set:
    with open(os.path.dirname(os.path.abspath(__file__)) + "/database/checked.txt", "wb") as f_out: f_out.write(us)

# Split by separator
unique_song_set = [us.split('<SEP>') for us in unique_song_set]

# Construct search list
for us in unique_song_set:
    us.append(
        'http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Ddigital-music&field-keywords=' +
        us[2].replace(' ', '+') + '+' + us[3].replace(' ', '+'))

download_links = []


class AmazonSpider(scrapy.Spider):
    name = "amazon"
    allowed_domains = ["amazon.com"]
    start_urls = None

    def start_requests(self):
        request = []
        for us in unique_song_set:
            request.append(scrapy.Request(us[4], callback=self.parse))
            request[len(request)-1].meta['us'] = us
        return request

    def parse(self, response):
        response.meta['us'].append(response.xpath('//tr[@id="result_0"]/td[1]/div/a/@flashurl').extract())


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

writeLog("Crawling started...")
process.crawl(AmazonSpider)
process.start()
writeLog("Crawling ended...")

for us in unique_song_set:
    if len(us[5]) == 0:
        writeLog('File: ' + us[2] + ' - ' + us[3] + ": NOT FOUND")

    else:
        response = urllib2.urlopen(us[5][0])
        track = response.read()

        directory = "/home/fajqa/Documents/Python/AmazonScraping/songs/" + us[0][2] + "/" + us[0][3] + "/" + us[0][4] + "/"
        if not os.path.exists(directory):
            os.makedirs(directory)
        os.chdir(directory)

        with open(us[0] + '.mp3', "wb") as f_out: f_out.write(track)

        writeLog('File: ' + us[2] + ' - ' + us[3] + ": SAVED")