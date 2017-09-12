# Load data
import numpy as np
from sklearn import datasets
iris = datasets.load_iris()
iris_X = iris.data
iris_y = iris.target


iris_X_train = iris_X[indices[:-15]]
iris_y_train = iris_y[indices[:-15]]
iris_X_test  = iris_X[indices[-25:]]
iris_y_test  = iris_y[indices[-25:]]

# Visualize data
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
X = iris.data[:, :2]  # we only take the first two features.
y = iris.target
x_min, x_max = X[:, 0].min() - .5, X[:, 0].max() + .5
y_min, y_max = X[:, 1].min() - .5, X[:, 1].max() + .5



""" Part 3 """
from sklearn import svm
svc = svm.SVC(kernel='linear')
svc.fit(iris_X_train, iris_y_train)  
svc.predict(iris_X_test)
print iris_y_test
