#!/home/chana/anaconda3/bin/python3.6
import pandas as pd
import numpy as np
import pymysql.cursors
from sklearn.cluster import KMeans  # KMeans clustering
import matplotlib.pyplot as plt
import sys
import json

data = pd.read_csv("/media/chana/Data/Level4/git/Moviesuggestion/clustering/kaggle/tbl_movie.csv")

data_use = data.ix[:,
           ['id','genre', 'key_words', 'title', 'director', 'imdb_rating', 'country', 'year', 'language', 'writter',
            'review_polarity','imdb_id']]

data_use['title'] = [i.replace("\xa0", "") for i in list(data_use['title'])]

# --------------------------------
print(data_use.shape)
clean_data = data_use.dropna(axis=0)
print(clean_data.shape)
clean_data = clean_data.drop_duplicates(['imdb_id'])
clean_data = clean_data.reset_index(drop=True)
print(clean_data.shape)

dataArray = clean_data.as_matrix(columns=None)
tempArray = []

i = 0
for m in dataArray:
    i += 1
    n = m.tolist()
    tempArray.append(n[11])


# --------------------------------
people_list = []
for i in range(clean_data.shape[0]):
    name1 = clean_data.ix[i, 'country'].replace(" ", "|")
    name2 = clean_data.ix[i, 'year'].replace(" ", "|")
    name3 = clean_data.ix[i, 'language'].replace(" ", "|")
    name4 = clean_data.ix[i, 'writter'].replace(" ", "|")
    name5 = clean_data.ix[i, 'director'].replace(" ", "|")
    name6 = str(clean_data.ix[i, 'imdb_rating'])
    name7 = str(clean_data.ix[i, 'review_polarity'])

    people_list.append("|".join([
        name1,
        name2,
        name3,
        name4,
        name5,
        name6,
        name7
    ]))
clean_data['movie'] = people_list

saveClusters = ("UPDATE tbl_movie SET cluster = %s WHERE imdb_id = %s")
findIdFromTitle = ('SELECT id FROM tbl_movie WHERE title = %s')
saveUserPrefs = ('UPDATE tbl_user SET recommonded_non_p = %s WHERE username = %s')

cnx = pymysql.connect(host='localhost', user='root', password='', db='movia',
                      charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
cursor = cnx.cursor()

# --------------------------------
from sklearn.feature_extraction.text import CountVectorizer


def token(text):
    return (text.split(","))


cv_kw = CountVectorizer(max_features=100, tokenizer=token)
keywords = cv_kw.fit_transform(clean_data["key_words"])
keywords_list = ["kw_" + i for i in cv_kw.get_feature_names()]

cv_ge = CountVectorizer(tokenizer=token)
genres = cv_ge.fit_transform(clean_data["genre"])
genres_list = ["genres_" + i for i in cv_ge.get_feature_names()]

cv_pp = CountVectorizer(max_features=100, tokenizer=token)
people = cv_pp.fit_transform(clean_data["movie"])
people_list = ["pp_" + i for i in cv_pp.get_feature_names()]

cluster_data = np.hstack([keywords.todense() * 5
                             , genres.todense() * 4
                             , people.todense() * 2
                          ])

criterion_list = keywords_list \
                 + genres_list \
                 + people_list

mod = KMeans(n_clusters=40, n_init=40, init='k-means++')

category = mod.fit_predict(cluster_data)


# find center of clusters
centers = mod.cluster_centers_

plt.figure(figsize=(10, 10))
plt.scatter(centers[:, 0], centers[:, 1], marker='x', s=169, linewidths=3,
            color='r', zorder=10)


category_dataframe = pd.DataFrame({"category": category}, index=clean_data['title'])
numpyMatrix = category_dataframe.as_matrix()
clean_data.ix[list(category_dataframe['category'] == 0),['title']]
mm = category_dataframe['category'].values.tolist()

results = [] # this is a dictionary

plt.show()
i = 0
for x in tempArray:
    print(mm[i])
    print(x)
    cursor.execute(saveClusters, (mm[i],x))
    cnx.commit()

    results.append({x:mm[i]})
    i += 1

print(results)

plt.show()


    # cursor.execute(saveClusters, [])
    # cnx.commit()


# print(numpyMatrix)

description = category_dataframe.describe()
print(description)

print(pd)
i = 0
for x in category_dataframe:
    print(x)
    # cursor.execute(saveClusters, (x[0], i))
    # cnx.commit()
    # i += 1

# --------------------------------
clean_data.ix[list(category_dataframe['category'] == 0), ['genres', 'key_words', 'movie']]


def recommend(movie_name, recommend_number=5):
    if movie_name in list(clean_data['title']):
        movie_cluster = category_dataframe.ix[movie_name, 'category']
        score = clean_data.ix[list(category_dataframe['category'] == movie_cluster), ['imdb_rating', 'title']]
        sort_score = score.sort_values(['imdb_rating'], ascending=[0])
        sort_score = sort_score[sort_score['title'] != movie_name]
        recommend_number = min(sort_score.shape[0], recommend_number)
        recommend_movie = list(sort_score.iloc[range(recommend_number), 1])
        return recommend_movie
    else:
        return ''


movieIdList = []


def saveMovies(movies):
    for movie in movies:
        cursor.execute(findIdFromTitle, movie)

        row = cursor.fetchone()
        movieIdList.append(row['id'])
    print(set(movieIdList))
    res = json.dumps(movieIdList)
    print(type('dkaka'))
    print(res)
    cursor.execute(saveUserPrefs, (res, sys.argv[1]))
    cnx.commit()


cont = len(sys.argv)
i = 2

movie_list = []

# while i < cont:
#     movie = sys.argv[i]
#     movie = movie.replace("\'", "__")
#     movie = movie.title()
#     recommends = recommend(movie, 50)
#     for rec in recommends:
#         movie_list.append(rec)
#     i += 1
#
# print(movie_list)
# saveMovies(movie_list)
