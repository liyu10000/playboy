from builtins import object
import numpy as np

from cs231n.layers import *
from cs231n.fast_layers import *
from cs231n.layer_utils import *


class ThreeLayerConvNet(object):
    """
    A three-layer convolutional network with the following architecture:

    conv - relu - 2x2 max pool - affine - relu - affine - softmax

    The network operates on minibatches of data that have shape (N, C, H, W)
    consisting of N images, each with height H and width W and with C input
    channels.
    """

    def __init__(self, input_dim=(3, 32, 32), num_filters=32, filter_size=7,
                 hidden_dim=100, num_classes=10, weight_scale=1e-3, reg=0.0,
                 dtype=np.float32):
        """
        Initialize a new network.

        Inputs:
        - input_dim: Tuple (C, H, W) giving size of input data
        - num_filters: Number of filters to use in the convolutional layer
        - filter_size: Size of filters to use in the convolutional layer
        - hidden_dim: Number of units to use in the fully-connected hidden layer
        - num_classes: Number of scores to produce from the final affine layer.
        - weight_scale: Scalar giving standard deviation for random initialization
          of weights.
        - reg: Scalar giving L2 regularization strength
        - dtype: numpy datatype to use for computation.
        """
        self.params = {}
        self.reg = reg
        self.dtype = dtype

        ############################################################################
        # TODO: Initialize weights and biases for the three-layer convolutional    #
        # network. Weights should be initialized from a Gaussian with standard     #
        # deviation equal to weight_scale; biases should be initialized to zero.   #
        # All weights and biases should be stored in the dictionary self.params.   #
        # Store weights and biases for the convolutional layer using the keys 'W1' #
        # and 'b1'; use keys 'W2' and 'b2' for the weights and biases of the       #
        # hidden affine layer, and keys 'W3' and 'b3' for the weights and biases   #
        # of the output affine layer.                                              #
        ############################################################################
        C, H, W = input_dim
        self.params['W1'] = weight_scale * np.random.randn(num_filters, C, filter_size, filter_size)
        self.params['b1'] = np.zeros(num_filters)
        self.params['W2'] = weight_scale * np.random.randn(int(num_filters*H/2*W/2), hidden_dim)  # problematic here, need to get output shape of conv layer and max pool layer (/2 here)
        self.params['b2'] = np.zeros(hidden_dim)
        self.params['W3'] = weight_scale * np.random.randn(hidden_dim, num_classes)
        self.params['b3'] = np.zeros(num_classes)
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        for k, v in self.params.items():
            self.params[k] = v.astype(dtype)


    def loss(self, X, y=None):
        """
        Evaluate loss and gradient for the three-layer convolutional network.

        Input / output: Same API as TwoLayerNet in fc_net.py.
        """
        W1, b1 = self.params['W1'], self.params['b1']
        W2, b2 = self.params['W2'], self.params['b2']
        W3, b3 = self.params['W3'], self.params['b3']

        # pass conv_param to the forward pass for the convolutional layer
        filter_size = W1.shape[2]
        conv_param = {'stride': 1, 'pad': (filter_size - 1) // 2}

        # pass pool_param to the forward pass for the max-pooling layer
        pool_param = {'pool_height': 2, 'pool_width': 2, 'stride': 2}

        scores = None
        ############################################################################
        # TODO: Implement the forward pass for the three-layer convolutional net,  #
        # computing the class scores for X and storing them in the scores          #
        # variable.                                                                #
        ############################################################################
        out_cv1, cache_cv1 = conv_forward_fast(X, W1, b1, conv_param)
        out_re1, cache_re1 = relu_forward(out_cv1)
        out_mp1, cache_mp1 = max_pool_forward_fast(out_re1, pool_param)
        out_af1, cache_af1 = affine_forward(out_mp1, W2, b2)
        out_re2, cache_re2 = relu_forward(out_af1)
        out_af2, cache_af2 = affine_forward(out_re2, W3, b3)
        scores = out_af2
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        if y is None:
            return scores

        loss, grads = 0, {}
        ############################################################################
        # TODO: Implement the backward pass for the three-layer convolutional net, #
        # storing the loss and gradients in the loss and grads variables. Compute  #
        # data loss using softmax, and make sure that grads[k] holds the gradients #
        # for self.params[k]. Don't forget to add L2 regularization!               #
        ############################################################################
        loss, dout = softmax_loss(scores, y)
        loss += 0.5 * self.reg * (np.sum(np.square(W1)) + np.sum(np.square(W2)) + np.sum(np.square(W3)))
        
        dout, dW3, db3 = affine_backward(dout, cache_af2)
        dout = relu_backward(dout, cache_re2)
        dout, dW2, db2 = affine_backward(dout, cache_af1)
        dout = max_pool_backward_fast(dout, cache_mp1)
        dout = relu_backward(dout, cache_re1)
        dout, dW1, db1 = conv_backward_fast(dout, cache_cv1)
        
        grads['W1'] = dW1 + self.reg * W1
        grads['b1'] = db1
        grads['W2'] = dW2 + self.reg * W2
        grads['b2'] = db2
        grads['W3'] = dW3 + self.reg * W3
        grads['b3'] = db3
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        return loss, grads



class ThreeLayerConvNetBN(object):
    """
    A three-layer convolutional network with the following architecture:

    conv - bn - relu - 2x2 max pool - affine - bn - relu - dropout - affine - softmax

    The network operates on minibatches of data that have shape (N, C, H, W)
    consisting of N images, each with height H and width W and with C input
    channels.
    """

    def __init__(self, input_dim=(3, 32, 32), num_filters=32, filter_size=7,
                 hidden_dim=100, num_classes=10, weight_scale=1e-3, reg=0.0,
                 dropout=0.5, dtype=np.float32):
        """
        Initialize a new network.

        Inputs:
        - input_dim: Tuple (C, H, W) giving size of input data
        - num_filters: Number of filters to use in the convolutional layer
        - filter_size: Size of filters to use in the convolutional layer
        - hidden_dim: Number of units to use in the fully-connected hidden layer
        - num_classes: Number of scores to produce from the final affine layer.
        - weight_scale: Scalar giving standard deviation for random initialization
          of weights.
        - reg: Scalar giving L2 regularization strength
        - dropout: Scalar between 0 and 1 giving dropout strength.
        - dtype: numpy datatype to use for computation.
        """
        self.params = {}
        self.reg = reg
        self.dtype = dtype
        self.dropout = dropout

        ############################################################################
        # TODO: Initialize weights and biases for the three-layer convolutional    #
        # network. Weights should be initialized from a Gaussian with standard     #
        # deviation equal to weight_scale; biases should be initialized to zero.   #
        # All weights and biases should be stored in the dictionary self.params.   #
        # Store weights and biases for the convolutional layer using the keys 'W1' #
        # and 'b1'; use keys 'W2' and 'b2' for the weights and biases of the       #
        # hidden affine layer, and keys 'W3' and 'b3' for the weights and biases   #
        # of the output affine layer.                                              #
        ############################################################################
        C, H, W = input_dim
        self.params['W1'] = weight_scale * np.random.randn(num_filters, C, filter_size, filter_size)
        self.params['b1'] = np.zeros(num_filters)
        self.params['gamma1'] = np.ones(num_filters)
        self.params['beta1'] = np.zeros(num_filters)
        self.params['W2'] = weight_scale * np.random.randn(int(num_filters*H/2*W/2), hidden_dim)  # problematic here, need to get output shape of conv layer and max pool layer (/2 here)
        self.params['b2'] = np.zeros(hidden_dim)
        self.params['gamma2'] = np.ones(hidden_dim)
        self.params['beta2'] = np.zeros(hidden_dim)
        self.params['W3'] = weight_scale * np.random.randn(hidden_dim, num_classes)
        self.params['b3'] = np.zeros(num_classes)

        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        for k, v in self.params.items():
            self.params[k] = v.astype(dtype)


    def loss(self, X, y=None):
        """
        Evaluate loss and gradient for the three-layer convolutional network.

        Input / output: Same API as TwoLayerNet in fc_net.py.
        """
        W1, b1 = self.params['W1'], self.params['b1']
        gamma1, beta1 = self.params['gamma1'], self.params['beta1']
        W2, b2 = self.params['W2'], self.params['b2']
        gamma2, beta2 = self.params['gamma2'], self.params['beta2']
        W3, b3 = self.params['W3'], self.params['b3']

        # pass conv_param to the forward pass for the convolutional layer
        filter_size = W1.shape[2]
        conv_param = {'stride': 1, 'pad': (filter_size - 1) // 2}
        
        # pass bn_param to the forward pass for the batch normalization layer after conv
        bn_param1 = {'mode': 'train' if y is not None else 'test'}

        # pass pool_param to the forward pass for the max-pooling layer
        pool_param = {'pool_height': 2, 'pool_width': 2, 'stride': 2}
        
        # pass bn_param to the forward pass for the batch normalization layer after affine
        bn_param2 = {'mode': 'train' if y is not None else 'test'}
        
        # pass dropout_param to the forward pass for the dropout layer
        dropout_param = {'mode': 'train' if y is not None else 'test', 'p': self.dropout}

        scores = None
        ############################################################################
        # TODO: Implement the forward pass for the three-layer convolutional net,  #
        # computing the class scores for X and storing them in the scores          #
        # variable.                                                                #
        ############################################################################
        out_cv1, cache_cv1 = conv_forward_fast(X, W1, b1, conv_param)
        out_bn1, cache_bn1 = spatial_batchnorm_forward(out_cv1, gamma1, beta1, bn_param1)
        out_re1, cache_re1 = relu_forward(out_bn1)
        out_mp1, cache_mp1 = max_pool_forward_fast(out_re1, pool_param)
        out_af1, cache_af1 = affine_forward(out_mp1, W2, b2)
        out_bn2, cache_bn2 = batchnorm_forward(out_af1, gamma2, beta2, bn_param2)
        out_re2, cache_re2 = relu_forward(out_bn2)
        out_dp1, cache_dp1 = dropout_forward(out_re2, dropout_param)
        out_af2, cache_af2 = affine_forward(out_dp1, W3, b3)
        scores = out_af2
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        if y is None:
            return scores

        loss, grads = 0, {}
        ############################################################################
        # TODO: Implement the backward pass for the three-layer convolutional net, #
        # storing the loss and gradients in the loss and grads variables. Compute  #
        # data loss using softmax, and make sure that grads[k] holds the gradients #
        # for self.params[k]. Don't forget to add L2 regularization!               #
        ############################################################################
        loss, dout = softmax_loss(scores, y)
        loss += 0.5 * self.reg * (np.sum(np.square(W1)) + np.sum(np.square(W2)) + np.sum(np.square(W3)))
        
        dout, dW3, db3 = affine_backward(dout, cache_af2)
        dout = dropout_backward(dout, cache_dp1)
        dout = relu_backward(dout, cache_re2)
        dout, dgamma2, dbeta2 = batchnorm_backward_alt(dout, cache_bn2)
        dout, dW2, db2 = affine_backward(dout, cache_af1)
        dout = max_pool_backward_fast(dout, cache_mp1)
        dout = relu_backward(dout, cache_re1)
        dout, dgamma1, dbeta1 = spatial_batchnorm_backward(dout, cache_bn1)
        dout, dW1, db1 = conv_backward_fast(dout, cache_cv1)
        
        grads['W1'] = dW1 + self.reg * W1
        grads['b1'] = db1
        grads['gamma1'] = dgamma1
        grads['beta1'] = dbeta1
        grads['W2'] = dW2 + self.reg * W2
        grads['b2'] = db2
        grads['gamma2'] = dgamma2
        grads['beta2'] = dbeta2
        grads['W3'] = dW3 + self.reg * W3
        grads['b3'] = db3
        ############################################################################
        #                             END OF YOUR CODE                             #
        ############################################################################

        return loss, grads
