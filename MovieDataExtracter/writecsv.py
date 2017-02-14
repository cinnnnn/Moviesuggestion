import csv

csvfile = open('names.csv','w')
fieldnames = ['first_name', 'last_name']
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
writer.writeheader()
writer.writerow({'first_name': 'aaa', 'last_name': 'bbb'})
writer.writerow({'first_name': 'ccc', 'last_name': 'ddd'})
writer.writerow({'first_name': 'eee', 'last_name': 'fff'})