import numpy as np

# Defining the sigmoid function for activations 
# 定义 sigmoid 激活函数
def sigmoid(x):
    return 1/(1+np.exp(-x))

# Derivative of the sigmoid function
# 激活函数的导数
def sigmoid_prime(x):
    return sigmoid(x) * (1 - sigmoid(x))

# Input data
# 输入数据
x = np.array([0.1, 0.3])
# Target
# 目标
y = 0.2
# Input to output weights
# 输入到输出的权重
weights = np.array([-0.8, 0.5])

# The learning rate, eta in the weight step equation
# 权重更新的学习率
learnrate = 0.5

# the linear combination performed by the node (h in f(h) and f'(h))
# 输入和权重的线性组合
# h = x[0]*weights[0] + x[1]*weights[1]
h = np.dot(x, weights)

# The neural network output (y-hat)
# 神经网络输出
nn_output = sigmoid(h)

# output error (y - y-hat)
# 输出误差
error = y - nn_output

# output gradient (f'(h))
# 输出梯度
output_grad = sigmoid_prime(h)

# error term (lowercase delta)
error_term = error * output_grad

# Gradient descent step 
# 梯度下降一步
# del_w = [ learnrate * error_term * x[0],
#           learnrate * error_term * x[1]]
del_w = learnrate * error_term * x

print('Neural Network output:')
print(nn_output)
print('Amount of Error:')
print(error)
print('Change in Weights:')
print(del_w)
