import random

from clustering import Clustering


def assigncentroids():
    print(1)


choices = [0, 1]

# print(random.choice(choices))

f = open("bitvector.txt", "r")

coordData = []

k = 0

randoCentroid = []

for line in f.readlines():

    k += 1

    row = line.split()

    intValues = []

    for i in row:

        intValues.append(int(i))

    coordData.append(intValues)

print(coordData)

for i in range(k):

    coOrd = []

    for j in range(k):

        coOrd.append(random.choice(choices))

    randoCentroid.append(coOrd)

print(randoCentroid)

Clusterings = []

for i in range(k):
    temp = Clustering(randoCentroid[i])
    Clusterings.append(temp)




