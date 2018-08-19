import numpy as np
from data_prep import features, targets, features_test, targets_test

n_rows, n_features = features.shape
weights = np.random.normal(scale=1/n_features**0.5, size=n_features)

epochs = 5000
learning_rate = 0.01
last_loss = None

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_prime(x):
	return sigmoid(x) / (1 - sigmoid(x))

def h(row, weights):
	return np.dot(row, weights)

def nn_output(row, weights):
	return sigmoid(h(row, weights))


for epoch in range(epochs):
	weights_step = np.zeros(n_features)
	for row,target in zip(features.values, targets):
		# calculate sum multiplication
		h = np.dot(weights, row)
		# calculate output
		nn_output = sigmoid(h)
		# calculate error term 
		error_term = (target - nn_output) * sigmoid_prime(h)
		# update weights step
		weights_step += error_term * row
	weights += learning_rate * weights_step / n_rows

	if epoch % (epochs/10) == 0:
		out = sigmoid(np.dot(features, weights))
		loss = np.mean((out - targets)**2)
		if last_loss and last_loss < loss:
			print("Train loss: {}. WARNING: loss increasing".format(loss))
		else:
			print("Train loss: {}".format(loss))
		last_loss = loss

# calculate accuracy on test data
test_out = sigmoid(np.dot(features_test, weights))
predictions = test_out > 0.5
accuracy = np.mean(predictions == targets_test)
print("Prediction accuracy: {:.3f}".format(accuracy))
