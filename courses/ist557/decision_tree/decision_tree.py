"""
Reference site link: https://medium.com/@penggongting/implementing-decision-tree-from-scratch-in-python-c732e7c69aea.
"""
import numpy as np


def entropy():
	pass

class DecisionTreeClassifier:
	def fit(self, max_depth, min_sample_leaf):
		self.dtree = Node(X, y, np.arange(len(y)), max_depth, min_sample_leaf)
		return self

	def predict(self, X):
		return self.dtree.predict(X)

class Node:
	def __init__(self, X, y, index, max_depth, min_sample_leaf):
		self.X = X
		self.y = y
		self.index = index
		self.max_depth = max_depth
		self.min_sample_leaf = min_sample_leaf
		self.row_count = len(index)
		self.col_count = X.shape[1]
		self.val = np.mean(y[index])
		self.score = float('inf')
		self.find_varsplit()

	