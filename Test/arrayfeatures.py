import json

jsonString = '{"18607":"4","18698":"2","21050":"4"}'

arr = json.loads(jsonString)

for element in arr:
    movieId = element
    print(movieId)
    rating = arr[element]
    print(rating)

