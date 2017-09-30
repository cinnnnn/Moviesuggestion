# This is the movie list path
import urllib.request
import pymysql.cursors
import json
from time import sleep

cnx = pymysql.connect(host='localhost', user='root', password='', db='movia',
                      charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

cursor = cnx.cursor()

getMovieQuery = ("SELECT * FROM tbl_movie WHERE imdb_id = %s")
saveMovieQuery = ("INSERT INTO `tbl_movie` (`title`, `imdb_id`, `country`, `actors`, `year`, "
                  "`plot`, `poster_url`, `genre`, `language`, `runtime`, `writer`, `director`,"
                  "`imdb_rating`, `imdb_votes`) "
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")


path = 'links.csv'

# Open movielist.csv file
data = open(path, 'r')

hasData = True

# while loop for extract every record in the movie list
while hasData:

    movieData = data.readline()
    if movieData and not movieData.isspace():
        movieData = movieData.split(',')

        movieImdbId = movieData[1]
        movieImdbId = "tt" + movieImdbId
        print(movieImdbId)

        cursor.execute(getMovieQuery, movieImdbId)

        rows = cursor.fetchall()
        # print('Total Row(s):', cursor.rowcount)

        # for (title, genre, plot) in cursor:
        #     print("%s  belongs to %s genres and plot is %s".format(title, genre, plot))

        # movieTitle = movieTitle.replace(" ", "+")
        i = 0

        if (cursor.rowcount < 1):
            try:
                # send rerquest to OMDB api and get movie info
                # movieInfo = urllib.request.urlopen("http://www.omdbapi.com/?t=%s&y=&plot=full&r=json" %
                #                                    movieTitle).read().decode("utf-8")
                i += 1
                print(i)

                try:
                    movieInfo = urllib.request.urlopen(
                        "http://www.omdbapi.com/?i=%s&plot=full&r=json" % movieImdbId).read().decode("utf-8")
                except ValueError:
                    sleep(10)
                    try:
                        movieInfo = urllib.request.urlopen(
                            "http://www.omdbapi.com/?i=%s&plot=full&r=json" % movieImdbId).read().decode("utf-8")
                    except ValueError:
                        sleep(20)
                        try:
                            movieInfo = urllib.request.urlopen(
                                "http://www.omdbapi.com/?i=%s&plot=full&r=json" % movieImdbId).read().decode("utf-8")
                        except ValueError:
                            sleep(30)
                            try:
                                movieInfo = urllib.request.urlopen(
                                    "http://www.omdbapi.com/?i=%s&plot=full&r=json" % movieImdbId).read().decode(
                                    "utf-8")
                            except ValueError:
                                sleep(60)
                                try:
                                    movieInfo = urllib.request.urlopen(
                                        "http://www.omdbapi.com/?i=%s&plot=full&r=json" % movieImdbId).read().decode(
                                        "utf-8")
                                except ValueError:
                                    sleep(180)
                                    movieInfo = urllib.request.urlopen(
                                        "http://www.omdbapi.com/?i=%s&plot=full&r=json" % movieImdbId).read().decode(
                                        "utf-8")

                movieJson = json.loads(movieInfo)
                print(movieJson)
                if (movieJson['Runtime'] == 'N/A'):
                    movieJson['Runtime'] = 0

                returnedMovieData = (movieJson['Title'], movieJson['imdbID'], movieJson['Country'],
                                     movieJson['Actors'], movieJson['Year'], movieJson['Plot'],
                                     movieJson['Poster'], movieJson['Genre'], movieJson['Language'],
                                     movieJson['Runtime'], movieJson['Writer'], movieJson['Director'],
                                     movieJson['imdbRating'],movieJson['imdbVotes'])

                # Insert new movie
                cursor.execute(saveMovieQuery, returnedMovieData)
                cnx.commit()


            except ValueError:
                print("Oops! That is an invalid Movie")



    else:
        hasData = False
        print('%s movies updated', format(i))

cursor.close()
cnx.close()
