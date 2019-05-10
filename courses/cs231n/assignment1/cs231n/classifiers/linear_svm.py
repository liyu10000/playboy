import numpy as np
from random import shuffle
from past.builtins import xrange

def svm_loss_naive(W, X, y, reg):
    """
    Structured SVM loss function, naive implementation (with loops).

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
    dW = np.zeros(W.shape) # initialize the gradient as zero

    # compute the loss and the gradient
    num_classes = W.shape[1]  # C
    num_features = W.shape[0] # D
    num_train = X.shape[0]  # N
    loss = 0.0
    for i in xrange(num_train):
        scores = X[i].dot(W)  # 1xD, DxC => 1xC
        correct_class_score = scores[y[i]]
        pos_margin_cnt = 0 # count for case v == y[i]
        for j in xrange(num_classes):
            if j == y[i]:
                continue
            margin = scores[j] - correct_class_score + 1 # note delta = 1
            if margin > 0:
                loss += margin

                pos_margin_cnt += 1

                # when v != y[i]
                for u in xrange(num_features):
                    dW[u][j] += X[i][u]

        # when v == y[i]
        for u in xrange(num_features):
            dW[u][y[i]] -= pos_margin_cnt * X[i][u]

    # Right now the loss is a sum over all training examples, but we want it
    # to be an average instead so we divide by num_train.
    loss /= num_train
    dW /= num_train

    # Add regularization to the loss.
    loss += reg * np.sum(W * W)
    dW += 2 * reg * W

    #############################################################################
    # TODO:                                                                     #
    # Compute the gradient of the loss function and store it dW.                #
    # Rather that first computing the loss and then computing the derivative,   #
    # it may be simpler to compute the derivative at the same time that the     #
    # loss is being computed. As a result you may need to modify some of the    #
    # code above to compute the gradient.                                       #
    #############################################################################
    
    return loss, dW


def svm_loss_vectorized(W, X, y, reg):
    """
    Structured SVM loss function, vectorized implementation.

    Inputs and outputs are the same as svm_loss_naive.
    """
    loss = 0.0
    dW = np.zeros(W.shape) # initialize the gradient as zero

    #############################################################################
    # TODO:                                                                     #
    # Implement a vectorized version of the structured SVM loss, storing the    #
    # result in loss.                                                           #
    #############################################################################
    num_train = X.shape[0]  # N
    scores_all = X.dot(W)
    correct_class_score_all = scores_all[range(num_train), y] # Select One Element in Each Row of a Numpy Array by Column Indices
    correct_class_score_all = np.reshape(correct_class_score_all, (-1, 1)) # Numpy reshape 1d to 2d array with 1 column
    margin_all = scores_all - correct_class_score_all + 1
    loss = margin_all[margin_all > 0].sum() - num_train
    loss /= num_train
    loss += reg * np.sum(W * W)
    #############################################################################
    #                             END OF YOUR CODE                              #
    #############################################################################


    #############################################################################
    # TODO:                                                                     #
    # Implement a vectorized version of the gradient for the structured SVM     #
    # loss, storing the result in dW.                                           #
    #                                                                           #
    # Hint: Instead of computing the gradient from scratch, it may be easier    #
    # to reuse some of the intermediate values that you used to compute the     #
    # loss.                                                                     #
    #############################################################################
    binary = np.maximum(margin_all, 0)
    binary[binary > 0] = 1
    row_sum = np.sum(binary, axis=1) - 1 # subtract the case j == y[i] itself
    binary[np.arange(num_train), y] = -row_sum.T
    dW = np.dot(X.T, binary)
    
#     num_classes = W.shape[1]  # C
#     for i in range(num_train):
#         for j in range(num_classes):
#             if j == y[i]:
#                 continue
#             if margin_all[i][j] > 0:
#                 dW[:, y[i]] -= X[i, :]
#                 dW[:, j] += X[i, :]
            
    dW /= num_train
    dW += 2 * reg * W
    #############################################################################
    #                             END OF YOUR CODE                              #
    #############################################################################

    return loss, dW
