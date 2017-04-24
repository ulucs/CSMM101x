import csv
import numpy as np
import sys


def evaluatestrue(inp):
    return (inp[3] * inp[0:3].dot(np.array([b, w1, w2]))) > 0

with open(sys.argv[1]) as csvin:
    data = csv.reader(csvin, delimiter=',', quotechar='"')
    inputs = []
    for row in data:
        row.insert(0, 1)
        inputs.append([float(j) for j in row])

w1 = np.random.rand()
w2 = np.random.rand()
b = np.random.rand()
tw1 = w1
tw2 = w2
tb = b

ins = np.array(inputs)

while not all([evaluatestrue(j) for j in ins]):
    for inp in ins:
        if not evaluatestrue(inp):
            tw1 += inp[1] * inp[3]
            tw2 += inp[2] * inp[3]
            tb += inp[0] * inp[3]
    w1 = tw1
    w2 = tw2
    b = tb

with open(sys.argv[2], 'a') as csvout:
    outp = csv.writer(csvout, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    outp.writerow([w1, w2, b])
