import re

import sys
import csv

csv.field_size_limit(sys.maxsize)

with open('ganeesha.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for rows in readCSV:
        reviews = rows[13]
        # print(rows[13])
        # characterDescription.split('\n',1)[0]
        # firstLine = characterDescription.splitlines()[0]
        # found = re.search(  "'u(.+?)u'", firstLine)

        #
        # pattern = re.compile("^\s+|\s*,\s*|\s+$")
        # mylist = ([x for x in pattern.split(text) if x])
        #

        reviesSet = reviews.split('</br></br></br></br></br></br></p>>')
        for review in reviesSet:
            review = review.replace('bound method Tag.get_text of', '')
            review = review.replace('<bound method Tag.get_text of <p><b>', '')
            review = review.replace('<br>', '')
            review = review.replace('a href=', '')
            review = review.replace('reviews-enter', '')
            review = review.replace('Add another review', '')
            review = review.replace('*** This review may contain spoilers ***', '')
            review = review.replace('\\n', '')
            review = review.replace('\\r', '')
            review = review.replace('\\', '')
            review = review.replace(',', '')
            review = review.replace('</b>', '')
            review = review.replace('</br>', '')
            review = review.replace('</p>', '')
            review = review.replace('<b>', '')
            review = review.replace('<p>', '')
            review = review.replace('[', '')
            review = review.replace('<', '')
            review = review.replace('>', '')
            print(review)

        print('#########################################################################################')
        # charName = charName.replace('_', '')
        # print(charName)










