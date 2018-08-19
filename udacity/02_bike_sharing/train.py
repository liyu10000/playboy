import numpy as np
from data_preparation import train_features, train_targets, val_features, val_targets
from NeuralNetwork import NeuralNetwork, MSE

### TODO:Set the hyperparameters here, you need to change the defalut to get a better solution ###
iterations = 5000
learning_rate = 0.1
hidden_nodes = 4
output_nodes = 1

N_i = train_features.shape[1]
network = NeuralNetwork(N_i, hidden_nodes, output_nodes, learning_rate)

losses = {'train':[], 'validation':[]}
for ii in range(iterations):
    # Go through a random batch of 128 records from the training data set
    batch = np.random.choice(train_features.index, size=128)
    X, y = train_features.ix[batch].values, train_targets.ix[batch]['cnt']

    network.train(X, y)
    
    # Printing out the training progress
    train_loss = MSE(network.run(train_features).T, train_targets['cnt'].values)
    val_loss = MSE(network.run(val_features).T, val_targets['cnt'].values)
    if ii % 100 == 0:
        print("Progress: {:4.1f}".format(100*ii/float(iterations)) \
                 + "% ... Training loss: " + str(train_loss)[:5] \
                 + " ... Validation loss: " + str(val_loss)[:5])
    
    losses['train'].append(train_loss)
    losses['validation'].append(val_loss)