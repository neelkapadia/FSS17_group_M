from sklearn import svm
import numpy as np
from sklearn import datasets
iris = datasets.load_iris()
iris_X = iris.data
iris_y = iris.target

print(iris.feature_names)
print(iris.target_names)
print(np.unique(iris_y))


svc = svm.SVC(kernel='rbf')
svc.fit(iris_X_train, iris_y_train)
svc.predict(iris_X_test)
print iris_y_test