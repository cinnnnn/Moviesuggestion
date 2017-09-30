import re

import sys
import csv

csv.field_size_limit(sys.maxsize)

with open('newRatings.csv', 'w') as outputFile:

    with open('ratings.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for rows in readCSV:
            movieLensId = rows[1]
            print(movieLensId)

            with open('links.csv') as idLinks:
                readLinks = csv.reader(idLinks, delimiter=',')
                for link in readLinks:
                    if(movieLensId == link[0]):
                        imdbId = link[1]
                        outputRow = rows[0]+',tt'+imdbId+','+rows[2]+'\n'
                        outputFile.write(outputRow)
