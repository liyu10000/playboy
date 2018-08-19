import numpy as np
from data_prep import features, targets, features_test, targets_test

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Hyperparameters
n_hidden = 2
epochs = 5000
learning_rate = 0.01

n_records, n_features = features.shape
last_loss = None

# initialize weights
weights_input_hidden = np.random.normal(scale=1/n_features**0.5, size=(n_features,n_hidden))
weights_hidden_output = np.random.normal(scale=1/n_features**0.5, size=n_hidden)

for epoch in range(epochs):
    delta_w_i_h = np.zeros(weights_input_hidden.shape)
    delta_w_h_o = np.zeros(weights_hidden_output.shape)
    for x, y in zip(features.values, targets):
        # forward propagation
        hidden_input = np.dot(x, weights_input_hidden)
        hidden_output = sigmoid(hidden_input)
        output_in = np.dot(hidden_output, weights_hidden_output)
        output_out = sigmoid(output_in)

        # backward propagation
        output_error = y - output_out
        output_error_term = output_error * output_out * (1 - output_out)

        hidden_error = np.dot(weights_input_hidden, output_error_term)
        hidden_error_term = hidden_error * hidden_output * (1 - hidden_output)

        delta_w_h_o += output_error_term * hidden_output
        delta_w_i_h += hidden_error_term * x[:, None]

    weights_input_hidden += learning_rate * delta_w_i_h / n_records
    weights_hidden_output += learning_rate * delta_w_h_o / n_records

    # Printing out the mean square error on the training set
    if epoch % (epochs / 10) == 0:
        hidden_output = sigmoid(np.dot(x, weights_input_hidden))
        out = sigmoid(np.dot(hidden_output, weights_hidden_output))
        loss = np.mean((out - targets) ** 2)
        if last_loss and last_loss < loss:
            print("Train loss: ", loss, "  WARNING - Loss Increasing")
        else:
            print("Train loss: ", loss)
        last_loss = loss

# Calculate accuracy on test data
hidden = sigmoid(np.dot(features_test, weights_input_hidden))
out = sigmoid(np.dot(hidden, weights_hidden_output))
predictions = out > 0.5
accuracy = np.mean(predictions == targets_test)
print("Prediction accuracy: {:.3f}".format(accuracy))