import csv
from collections import defaultdict

firstTryList =[]
secondTryList =[]
with open('clusterComparision.csv') as csvfile:
 readCSV = csv.reader(csvfile, delimiter=',')
 for rows in readCSV:
     firstTry = rows[0]
     secondTry = rows[1]
     firstTryList.append(firstTry)
     secondTryList.append(secondTry)

intersectedList = filter(lambda x:x in firstTryList, secondTryList)
count = len(intersectedList)
print int(count)


# d = defaultdict(int)
# for i in intersectedList:
#     d[i] += 1
#     result = max(d.iteritems(), key=lambda x: x[1])
# intersectedAmount = int(result[0])
# print intersectedAmount
# print result

print "{0:.2f}%".format(count/100 * 100)

# accuracy = float((intersectedAmount/count)*(100))

