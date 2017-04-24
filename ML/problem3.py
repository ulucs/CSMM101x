import csv
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier


def getscore(pred, actual):
    i = range(len(pred))
    return sum([1. for j in i if not pred[j] + actual[j] == 1]) / len(pred)


X = []
y = []

with open('input3.csv') as csvinput:
    data = csv.reader(csvinput)
    for row in data:
        y.append(float(row.pop()))
        X.append([float(j) for j in row])

X = np.array(X)
y = np.array(y)

trainX, testX, trainY, testY = train_test_split(X, y, test_size=0.4)

svr = SVC()
clfl = GridSearchCV(svr, {
    'kernel': ['linear'], 'C': [0.1, 0.5, 1, 5, 10, 50, 100]}, cv=5)
clfl.fit(trainX, trainY)
print "svm_linear,%f,%f" % (clfl.best_score_, getscore(clfl.predict(testX), testY))

clfp = GridSearchCV(svr, {
    'C': [0.1, 1, 3], 'gamma': [0.1, 1], 'degree': [4, 5, 6]}, cv=5)
clfp.fit(trainX, trainY)
print "svm_polynomial,%f,%f" % (clfp.best_score_, getscore(clfp.predict(testX), testY))

clfr = GridSearchCV(svr, {
    'kernel': ['rbf'], 'C': [0.1, 0.5, 1, 5, 10, 50, 100], 'gamma': [0.1, 0.5, 1, 3, 6, 10]}, cv=5)
clfr.fit(trainX, trainY)
print "svm_rbf,%f,%f" % (clfr.best_score_, getscore(clfr.predict(testX), testY))

logr = LogisticRegression()
clflr = GridSearchCV(logr, {'C': [0.1, 0.5, 1, 5, 10, 50, 100]}, cv=5)
clflr.fit(trainX, trainY)
print "logistic,%f,%f" % (clflr.best_score_, getscore(clflr.predict(testX), testY))

knn = KNeighborsClassifier()
clknn = GridSearchCV(knn, {'n_neighbors': range(1, 51), 'leaf_size': range(5, 61, 5)})
clknn.fit(trainX, trainY)
print "knn,%f,%f" % (clknn.best_score_, getscore(clknn.predict(testX), testY))

dect = DecisionTreeClassifier()
trec = GridSearchCV(dect, {'max_depth': range(1, 51), 'min_samples_split': range(2, 11)})
trec.fit(trainX, trainY)
print "decision_tree,%f,%f" % (trec.best_score_, getscore(trec.predict(testX), testY))

rfcl = RandomForestClassifier()
focl = GridSearchCV(rfcl, {'max_depth': range(1, 51), 'min_samples_split': range(2, 11)})
focl.fit(trainX, trainY)
print "random_forest,%f,%f" % (focl.best_score_, getscore(focl.predict(testX), testY))
