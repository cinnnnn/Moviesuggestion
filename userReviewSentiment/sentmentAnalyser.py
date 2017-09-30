#!/home/chana/anaconda3/bin/python3.6
##Author:Xing Lan
##TPC:Big data analysis
##Load naive bayes model

import os
import nltk
import pickle
import pymysql.cursors
import sys
import csv

csv.field_size_limit(sys.maxsize)

##set the working dictionary
os.chdir("/media/chana/Data/Level4/git/Moviesuggestion/userReviewSentiment")


#load classifier
f = open('naivebayes_classifier.pickle', 'rb')
classifier = pickle.load(f)
f.close()


savePolarity = ("UPDATE tbl_movie SET review_polarity = %s WHERE imdb_id = %s")
cnx = pymysql.connect(host='localhost', user='root', password='', db='movia',
                      charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
cursor = cnx.cursor()


def extract_features(document):
    document_words = set(document)    ##Distinct
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

word_features = []

text_file = open("word_features.txt", "r")
words = text_file.readline()
word_features=words.split() 
text_file.close()

with open('data/movieDataSet10.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for rows in readCSV:
        if len(rows) == 14:

            reviews = rows[13]
            # print(rows[13])
            # characterDescription.split('\n',1)[0]
            # firstLine = characterDescription.splitlines()[0]
            # found = re.search(  "'u(.+?)u'", firstLine)

            #
            # pattern = re.compile("^\s+|\s*,\s*|\s+$")
            # mylist = ([x for x in pattern.split(text) if x])
            #

            i = 0
            score = 0
            polarity = 0
            reviesSet = reviews.split('</br></br></br></br></br></br></p>>')
            for review in reviesSet:
                # Data Preprocessing
                review = review.replace('bound method Tag.get_text of', '')
                # review = review.replace('<bound method Tag.get_text of <p><b>', '')
                review = review.replace('<br>', '')
                review = review.replace('a href=', '')
                review = review.replace('reviews-enter', '')
                review = review.replace('Add another review', '')
                review = review.replace('*** This review may contain spoilers ***', '')
                review = review.replace('\\n', ' ')
                review = review.replace('\\r', ' ')
                review = review.replace('/a', ' ')
                review = review.replace('\"', ' ')
                review = review.replace('\'', ' ')
                review = review.replace('\\', '')
                review = review.replace(',', '')
                review = review.replace('</b>', '')
                review = review.replace('</br>', ' ')
                review = review.replace('</p>', ' ')
                review = review.replace('<b>', '')
                review = review.replace('<p>', ' ')
                review = review.replace('[', '')
                review = review.replace(']', '')
                review = review.replace('<', '')
                review = review.replace('         ', '')
                review = review.replace('        ', '')
                review = review.replace('       ', '')
                review = review.replace('      ', '')
                review = review.replace('     ', '')
                review = review.replace('    ', '')
                review = review.replace('   ', '')
                review = review.replace('  ', '')
                review = review.replace('>', '')
                if review == '' or review == '  ':
                    print(review)
                else:
                    sentenceSet = review.split('.')
                    for sentence in sentenceSet:
                        polarity += classifier.classify(extract_features(review.split()))
                        i += 1


            movieTitle = rows[1]
            movieId = rows[0]
            movieId = movieId.replace('http://www.imdb.com/title/','')
            movieId = movieId.replace('/?','')
            print('movie Id is : '+movieId)
            score = polarity/i
            print('score for the '+movieTitle+' is :')
            print(score)
            cursor.execute(savePolarity, (score, movieId))
            cnx.commit()

            print('#########################################################################################')
