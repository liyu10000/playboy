import numpy as np
from random import shuffle
from past.builtins import xrange

def softmax_loss_naive(W, X, y, reg):
    """
    Softmax loss function, naive implementation (with loops)

    Inputs have dimension D, there are C classes, and we operate on minibatches
    of N examples.

    Inputs:
    - W: A numpy array of shape (D, C) containing weights.
    - X: A numpy array of shape (N, D) containing a minibatch of data.
    - y: A numpy array of shape (N,) containing training labels; y[i] = c means
    that X[i] has label c, where 0 <= c < C.
    - reg: (float) regularization strength

    Returns a tuple of:
    - loss as single float
    - gradient with respect to weights W; an array of same shape as W
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using explicit loops.     #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    num_classes = W.shape[1]  # C
    num_features = W.shape[0] # D
    num_train = X.shape[0]  # N

    for i in xrange(num_train):
        fi = X[i].dot(W)  # 1xD, DxC => 1xC
        fi -= np.max(fi)
        fi_exp_sum = np.sum(np.exp(fi))
        loss += -fi[y[i]] + np.log(fi_exp_sum)
        
        for v in xrange(num_classes):
            factor = np.exp(fi[v]) / fi_exp_sum
            if v == y[i]:
                factor -= 1
            dW[:, v] += factor * X[i, :]

    loss /= num_train
    dW /= num_train
    
    loss += reg * np.sum(W * W)
    dW += 2 * reg * W
    #############################################################################
    #                          END OF YOUR CODE                                 #
    #############################################################################

    return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
    """
    Softmax loss function, vectorized version.

    Inputs and outputs are the same as softmax_loss_naive.
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    num_train = X.shape[0]  # N
    f = X.dot(W)
    f -= np.max(f, axis=1, keepdims=True)
    f_exp = np.exp(f)
    f_exp_sum = np.sum(f_exp, axis=1, keepdims=True)
    loss += np.sum(np.log(f_exp_sum))
    loss -= np.sum(f[np.arange(num_train), y])
    
    loss /= num_train
    loss += reg * np.sum(W * W)
    
    factor = f_exp / f_exp_sum
    factor[np.arange(num_train), y] -= 1
    dW = np.dot(X.T, factor)
    
    dW /= num_train
    dW += 2 * reg * W
    #############################################################################
    #                          END OF YOUR CODE                                 #
    #############################################################################

    return loss, dW

