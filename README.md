What are you looking at is a script made to scrape music samples from Amazon website.
1. Run "CheckForRepetitions.py" using command "python CheckForRepetitions.py".
It will get songs IDs from "msd_acquired.txt" and prepare a new "amazon_tracks.txt" set based on "unique_tracks.txt" but without songs that are already downloaded.
2. Run "AmazonScraping.py" using command "python AmazonScraping.py > log.txt".
It will download songs listed in a "amazon_tracks.txt" set, and save console output to "log.txt" file.
3. Command "grep -Po "(?<=\[SAVED\]\s).*(?=\s\[ARTIST\])" log.txt >> database/msd_acquired.txt" will append "msd_acquired.txt" with IDs of songs that have been just downloaded.
4. Command "grep "ERROR" log.txt >> error.txt" will print out in "error.txt" file the error messages, that you have to check individually and manually append "msd_acquired.txt" with .mp3 file name if the song is correct.
5. Repeat these steps till you are satisfied with results.
