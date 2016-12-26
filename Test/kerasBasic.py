import numpy
from keras.layers import Dense
from keras.models import Sequential

seed = 7
numpy.random.seed(seed)

dataSet = numpy.loadtxt("pima-indians-diabetes.csv", delimiter=",")

x = dataSet[:,0:8]
y = dataSet[:,8]

model = Sequential()
model.add(Dense(12, input_dim=8, init='uniform', activation='relu'))
model.add(Dense(8, init='uniform', activation='relu'))
model.add(Dense(1, init='uniform', activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit(x, y, nb_epoch=800, batch_size=10)

scores = model.evaluate(x,y)
print("%s: %.2f%%" %(model.metrics_names[1], scores[1]*100))







