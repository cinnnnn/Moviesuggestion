from keras.datasets import imdb
from keras.preprocessing import sequence
from keras.models import load_model

# load the dataset but only keep the top n words, zero the rest
top_words = 20000
(X_train, y_train), (X_test, y_test) = imdb.load_data(nb_words=top_words)

# truncate and pad input sequences
max_review_length = 500

X_test = sequence.pad_sequences(X_test, maxlen=max_review_length)

model = load_model('TrainedSentimentAnalysisModel.h5')

print("after loading model")

scores = model.evaluate(X_test, y_test, verbose=0)
print("Accuracy: %.2f%%" % (scores[1]*100))


