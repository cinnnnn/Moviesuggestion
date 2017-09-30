from __future__ import absolute_import
from __future__ import print_function
import six
__author__ = 'a_medelyan'

import rake
import operator
import io
import pymysql.cursors


# database connection
cnx = pymysql.connect(host='localhost', user='root', password='', db='movia',
                      charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
cursor = cnx.cursor()

def extractWords(text):
    # Stop word list
    stoppath = "SmartStoplist.txt"

    # 1. initialize RAKE by providing a path to a stopwords file
    rake_object = rake.Rake(stoppath, 3, 2, 1)

    # 1. Split text into sentences
    sentenceList = rake.split_sentences(text)

    for sentence in sentenceList:
        print("Sentence:", sentence)

    # generate candidate keywords
    stopwordpattern = rake.build_stop_word_regex(stoppath)
    phraseList = rake.generate_candidate_keywords(sentenceList, stopwordpattern)
    print("Phrases:", phraseList)

    # calculate individual word scores
    wordscores = rake.calculate_word_scores(phraseList)

    # generate candidate keyword scores
    keywordcandidates = rake.generate_candidate_keyword_scores(phraseList, wordscores)
    for candidate in keywordcandidates.keys():
        print("Candidate: ", candidate, ", score: ", keywordcandidates.get(candidate))

    # sort candidates by score to determine top-scoring keywords
    sortedKeywords = sorted(six.iteritems(keywordcandidates), key=operator.itemgetter(1), reverse=True)
    totalKeywords = len(sortedKeywords)

    # for example, you could just take the top third as the final keywords
    for keyword in sortedKeywords[0:int(totalKeywords / 3)]:
        print("Keyword: ", keyword[0], ", score: ", keyword[1])

    return (rake_object.run(text))
    # return stop_word_pattern

getMoviePlot = ("SELECT plot,key_words FROM tbl_movie WHERE imdb_id = %s")
saveKeyWords = ("UPDATE tbl_movie SET key_words = %s WHERE imdb_id = %s")

path = 'links.csv'

# Open movielist.csv file
data = open(path, 'r')

hasData = True

while hasData:

    movieData = data.readline()
    if movieData and not movieData.isspace():
        movieData = movieData.split(',')

        movieImdbId = movieData[1]
        movieImdbId = "tt" + movieImdbId
        print(movieImdbId)

        cursor.execute(getMoviePlot, movieImdbId)

        rows = cursor.fetchall()

        if(cursor.rowcount== 1):

            if(rows[0]['key_words'] == ''):

                text = rows[0]['plot']

                keywords = extractWords(text)

                decoded = ([[word for word in sets] for sets in keywords])

                keyWordSet = ''

                for words in decoded:
                    keyWordSet = keyWordSet + ',' + words[0]

                print(keyWordSet.replace(',','',1))

                result = keyWordSet.replace(',','',1)

                cursor.execute(saveKeyWords,(result,movieImdbId))
                cnx.commit()

            else:
                print("Keywords Already Extracted")
        else:
            print("Movie not found in db")

    else:
        hasData = False

cursor.close()
cnx.close()

print('Finished Updating')

# print ('f\xc3\xa1cil'.decode("utf8"))

# 1. initialize RAKE by providing a path to a stopwords file
# rake_object = rake.Rake(stoppath, 5, 3, 4)

# 2. run on RAKE on a given text
# sample_file = io.open("data/docs/fao_test/w2167e.txt", 'r',encoding="iso-8859-1")
# text = sample_file.read()
#
# keywords = rake_object.run(text)
#
# # 3. print results
# print("Keywords:", keywords)

# print("----------")
# EXAMPLE TWO - BEHIND THE SCENES (from https://github.com/aneesha/RAKE/rake.py)

