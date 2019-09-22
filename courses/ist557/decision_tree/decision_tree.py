"""
Reference site link: https://medium.com/@penggongting/implementing-decision-tree-from-scratch-in-python-c732e7c69aea.
"""
import numpy as np
from sklearn.datasets import load_iris
from pprint import pprint


class Entropy:
	def __init__(self, y_true, y_pred):
		"""
		:param y_true: values of selected rows, can be multi class
		:param y_pred: split decision, true or false
		:return score: return impurity score calculated by entropy method
		"""
		self.y_true = y_true
		self.y_pred = y_pred

	def calc(self):
		left_s, left_n = self.calc_(self.y_true[self.y_pred])
		right_s, right_n = self.calc_(self.y_true[~self.y_pred])
		score = (left_s * left_n + right_s * right_n) / (left_n + right_n)
		return score

	def calc_(self, division):
		count = np.unique(division, return_index=False, return_counts=True)[1]
		n = len(division)
		score = - np.sum(np.log2(count/n))
		return score, n


class DecisionTreeClassifier:
	def __init__(self, max_depth=5, min_samples_leaf=15):
		self.max_depth = max_depth
		self.min_samples_leaf = min_samples_leaf
		self.dtree = None

	def find_bestsplit(self, X, y):
		col_index = -1
		cutoff = None
		min_impurity = float('inf')
		for i, x in enumerate(X.T):
			for val in x:
				y_pred = x <= val
				impurity = Entropy(y, y_pred).calc()
				if impurity == 0:  # stop when perfect split reached
					return i, val, impurity
				if min_impurity > impurity:
					min_impurity = impurity
					col_index = i
					cutoff = val
		return col_index, cutoff, min_impurity

	def fit(self, X, y, depth=0):
		"""
		:param X: feature set
		:param y: target variable
		:param depth: the depth of current layer
		"""
		# minimum samples of leaf reached
		if len(y) == 0:
			return None
		elif len(y) <= self.min_samples_leaf:  
			return {'val': np.round(np.mean(y))}
		# all labels are the same in a group
		if np.all(y == y[0]):
			return {'val': y[0]}
		# max depth reached
		if depth >= self.max_depth: 
			return None
		# recursively generate trees
		col_index, cutoff, impurity = self.find_bestsplit(X, y)
		# par_node: will be the tree generated for given X and y
		par_node = {'col_index': col_index, 'cutoff': cutoff, 'val': np.round(np.mean(y))}
		left_split = X[:, col_index] <= cutoff
		right_split = X[:, col_index] > cutoff
		par_node['left'] = self.fit(X[left_split], y[left_split], depth + 1)
		par_node['right'] = self.fit(X[right_split], y[right_split], depth + 1)
		self.dtree = par_node
		return par_node

	def predict(self, X):
		y = np.zeros(X.shape[0])
		for i, row in enumerate(X):
			cur_layer = self.dtree
			while cur_layer:
				if not 'col_index' in cur_layer:
					y[i] = cur_layer['val']
					break
				var = cur_layer['val']
				if row[cur_layer['col_index']] <= cur_layer['cutoff']:
					cur_layer = cur_layer['left']
				else:
					cur_layer = cur_layer['right']
			else:
				y[i] = var
		return y

	def evaluate(self, X, y_true):
		y_pred = self.predict(X)
		accuracy = sum(y_true == y_pred) / len(y_true)
		return accuracy


if __name__ == '__main__':
	iris = load_iris()

	X = iris.data
	y = iris.target
	print(X.shape, y.shape) # (150, 4), (150,)

	clf = DecisionTreeClassifier(max_depth=6, min_samples_leaf=10)
	m = clf.fit(X[:120, :], y[:120])

	pprint(m)

	acc = clf.evaluate(X[120:, :], y[120:])
	print(acc)