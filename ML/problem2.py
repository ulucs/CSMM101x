import csv
import numpy as np
import sys


def getloss(pred, actual):
    diff = pred - actual
    return np.sum(diff * diff) / 2 / np.size(diff)


def updateparameters(ws, x, pred, actual, lr):
    dw = lr / np.size(pred) * np.matmul([(pred - actual)], x)[0]
    return ws - dw


def forward(ws, x):
    return np.matmul(x, ws)

xs = []
ys = []

with open(sys.argv[1]) as inputcsv:
    data = csv.reader(inputcsv)
    for row in data:
        ys.append(float(row.pop()))
        row.insert(0, np.random.rand())
        xs.append([float(j) for j in row])

xs = np.array(xs)
ys = np.array(ys)

# data normalization
xs = (xs - xs.mean(axis=0, keepdims=True)) / xs.std(axis=0, keepdims=True)
ys = (ys - ys.mean(axis=0, keepdims=True)) / ys.std(axis=0, keepdims=True)
# and set the intercept
xs[:, 0].fill(1)

for alpha in [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1., 5., 10.]:
    weights = np.zeros(3)
    for i in range(100):
        yhat = forward(weights, xs)
        weights = updateparameters(weights, xs, yhat, ys, alpha)

    with open('output2.csv', 'a') as outputcsv:
        outp = csv.writer(outputcsv)
        outp.writerow([alpha, 100, weights[0], weights[1], weights[2]])

weights = np.zeros(3)
for i in range(200):
    yhat = forward(weights, xs)
    weights = updateparameters(weights, xs, yhat, ys, 0.7)

with open(sys.argv[2], 'a') as outputcsv:
    outp = csv.writer(outputcsv)
    outp.writerow([0.7, 200, weights[0], weights[1], weights[2]])
