# This is the movie list path
import urllib.request
import pymysql
import json
from time import sleep


cnx = pymysql.connect(host='localhost', user='root', password='123', db='movia',
                      charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

cursor = cnx.cursor()




getMovieQuery = ("SELECT * FROM tbl_movie WHERE imdb_id = %s")
saveMovieQuery = ("INSERT INTO `tbl_movie` (`title`, `imdb_id`, `country`, `actors`, `year`, "
                  "`plot`, `poster_url`, `genre`, `language`, `runtime`, `writer`, `director`) "
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

saveMovieProfileQuery = ("INSERT INTO `tbl_movie_profile` (`imdb_id`, `imdb_rating`) "
                  "VALUES (%s, %s)")


getMovieProfileQuery = ("SELECT * FROM tbl_movie_profile WHERE imdb_id = %s")
path = 'links.csv'

# Open movielist.csv file
data = open(path,'r')

hasData = True

# while loop for extract every record in the movie list
while hasData:

    movieData = data.readline()
    if movieData and not movieData.isspace():
        movieData = movieData.split(',')

        movieImdbId = movieData[1]
        movieImdbId = "tt"+ movieImdbId
        print(movieImdbId)

        cursor.execute(getMovieQuery,movieImdbId)

        rows = cursor.fetchall()
        print('Total Row(s):', cursor.rowcount)

        # for (title, genre, plot) in cursor:
        #     print("%s  belongs to %s genres and plot is %s".format(title, genre, plot))

        # movieTitle = movieTitle.replace(" ", "+")

        if(cursor.rowcount<1):
            try:
                # send rerquest to OMDB api and get movie info
                # movieInfo = urllib.request.urlopen("http://www.omdbapi.com/?t=%s&y=&plot=full&r=json" %
                #                                    movieTitle).read().decode("utf-8")


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
                if(movieJson['Runtime']== 'N/A'):
                    movieJson['Runtime'] = 0


                returnedMovieData = (movieJson['Title'],movieJson['imdbID'],movieJson['Country'],
                                     movieJson['Actors'],movieJson['Year'],movieJson['Plot'],
                                     movieJson['Poster'],movieJson['Genre'],movieJson['Language'],
                                     movieJson['Runtime'],movieJson['Writer'],movieJson['Director'],)


                # Insert new movie
                cursor.execute(saveMovieQuery, returnedMovieData)
                cnx.commit()


            except ValueError:
                print("Oops! That is an invalid Movie")

        cursor.execute(getMovieProfileQuery, movieImdbId)
        rows = cursor.fetchall()

        if (cursor.rowcount < 1):

            try:

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
                        movieInfo = urllib.request.urlopen(
                            "http://www.omdbapi.com/?i=%s&plot=full&r=json" % movieImdbId).read().decode("utf-8")


                movieJson = json.loads(movieInfo)
                print(movieJson)
                imdbRating = movieJson['imdbRating']
                cursor.execute(saveMovieProfileQuery, (movieImdbId, imdbRating))
                cnx.commit()

            except ValueError:
                print("data insertion failed")



    else:
        hasData = False


cursor.close()
cnx.close()