# This is the movie list path
import urllib.request

path = '/media/chana/Data/Level4/git/Moviesuggestion/MovieDataExtracter/movielist.csv'

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
    #     send rerquest to OMDB api and get movie info
    #     movieInfo = urllib.request.urlopen("http://www.omdbapi.com/?t='Leap+Year'&y=&plot=full&r=json").read()

        print(movieTitle)
        try:
            movieInfo = urllib.request.urlopen("http://www.omdbapi.com/?t=%s&y=&plot=full&r=json" % movieTitle).read()
            print(movieInfo)
        except ValueError:
            print("Oops! That is an invalid Movie")

    #     Write extracted movie info to a file or send to a database


    else:
        hasData = False

