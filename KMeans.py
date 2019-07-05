import random
import math
import sys
from clustering import Clustering


def assigncentroids(clusterings, coorddata, kmeans):

    curmeans = []

    for i2 in clusterings:
        curmeans.append(i2.mean)

    for j2 in range(len(coorddata[0])):
        curcoords = []
        minCluster = 0
        for l in range(kmeans):
            curcoords.append(coorddata[l][j2])
        minDist = sys.maxsize
        for j3 in range(len(curmeans)):
            dist = euclidean(curcoords, curmeans[j3])

            if dist < minDist:
                minDist = dist
                minCluster = j3
        clusterings[minCluster].points.append(j2)


def euclidean(point1, point2):
    totaltemp = 0
    for i3 in range(len(point1)):
        totaltemp += abs(point1[i3]-point2[i3])**2
    return math.sqrt(totaltemp)




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

assigncentroids(Clusterings, coordData, k)

for clusterers in Clusterings:
    print(clusterers.points)


