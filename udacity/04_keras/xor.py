import numpy as np
from keras.utils import np_utils

# Set random seed
np.random.seed(42)

# Our data
X = np.array([[0,0],[0,1],[1,0],[1,1]]).astype('float32')
y = np.array([[0],[1],[1],[0]]).astype('float32')
# One-hot encoding the output
y = np_utils.to_categorical(y)


from keras.models import Sequential
from keras.layers.core import Dense, Activation

model = Sequential()
model.add(Dense(8, input_dim=2))
model.add(Activation("softmax"))
model.add(Dense(2))
model.add(Activation("softmax"))
model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
model.summary()
history = model.fit(X, y, epochs=1000, verbose=1)
score = model.evaluate(X, y)

print("\nAccuracy: ", score[-1])
print("\nPredictions:")
print(model.predict_proba(X))
