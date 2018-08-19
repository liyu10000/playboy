import numpy as np

def sigmoid(x):
    """
    Calculate sigmoid
    """
    return 1 / (1 + np.exp(-x))


input_layer_input = np.array([0.5, 0.1, -0.2])
input_layer_output = input_layer_input
target = 0.6
learnrate = 0.5

weights_input_hidden = np.array([[0.5, -0.6],
                                 [0.1, -0.2],
                                 [0.1, 0.7]])
weights_hidden_output = np.array([0.1, -0.3])

# forward
hidden_layer_input = np.dot(input_layer_input, weights_input_hidden)
hidden_layer_output = sigmoid(hidden_layer_input)

output_layer_in = np.dot(hidden_layer_output, weights_hidden_output)
output_layer_out = sigmoid(output_layer_in)
print("output:", output_layer_out)

# backward
output_error = target - output_layer_out
output_error_term = output_error * output_layer_out * (1 - output_layer_out)

hidden_error_term = weights_hidden_output * output_error_term * hidden_layer_output * (1 - hidden_layer_output)
print("hidden error term: ", hidden_error_term)

delta_w_h_o = learnrate * output_error_term * hidden_layer_output
delta_w_i_h = learnrate * hidden_error_term * input_layer_output[:, None]
print('Change in weights for hidden layer to output layer:', delta_w_h_o)
print('Change in weights for input layer to hidden layer:', delta_w_i_h)