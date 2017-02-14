# This is the movie list path
import urllib.request

import json
import csv

path = 'movielist.csv'
#path = '/media/chana/Data/Level4/git/Moviesuggestion/MovieDataExtracter/movielist.csv'

# Open movielist.csv file
data = open(path,'r')
plot = "full"
type = "json"

hasData = True

# while loop for extract every record in the movie list
while hasData:

    movieData = data.readline()
    if movieData and not movieData.isspace():
        movieData = movieData.split(',')

        movieTitle = movieData[0]
        movieYear = movieData[1]

        movieTitle = movieTitle.replace(" ", "+")


        print(movieTitle)
        try:
                # send rerquest to OMDB api and get movie info
            # movieInfo = urllib.request.urlopen("http://www.omdbapi.com/?t=%s&y=&plot=full&r=json" %
            #                                    movieTitle).read().decode("utf-8")
            # movieJson = json.loads(movieInfo)
            with open('../Data/movieData.csv', 'w') as csvfile:
                fieldnames = ['first_name', 'last_name']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
                writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
                writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})
            # print(movieJson)
        except ValueError:
            print("Oops! That is an invalid Movie")

    #     Write extracted movie info to a file or send to a database




    else:
        hasData = False

