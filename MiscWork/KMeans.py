import random
import math
import sys
import copy
import matplotlib.pyplot as plt
from MiscWork.clustering import Clustering

choices = [0, 1]


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
            if dist == minDist:
                randomchoice = random.choice(choices)
                if (randomchoice == 1):
                    minCluster = j3

            elif dist < minDist:
                minDist = dist
                minCluster = j3
        clusterings[minCluster].points.append(j2)


def reassigncentroids(clusterings, coorddata, kmeans):
    print("\n New Centroid Points")

    curmeans = []
    tempcopycluster = copy.deepcopy(clusterings)
    changed = 0

    for i2 in range(len(clusterings)):
        curmeans.append(clusterings[i2].mean)
        clusterings[i2].points = []

    for j2 in range(len(coorddata[0])):
        curcoords = []
        minCluster = 0
        for l in range(kmeans):
            curcoords.append(coorddata[l][j2])
        minDist = sys.maxsize
        for j3 in range(len(curmeans)):
            dist = euclidean(curcoords, curmeans[j3])
            if dist == minDist:
                randomchoice = random.choice(choices)
                if (randomchoice == 1):
                    minCluster = j3

            elif dist < minDist:
                minDist = dist
                minCluster = j3
        clusterings[minCluster].points.append(j2)
        if j2 not in tempcopycluster[minCluster].points:
            changed += 1
    for cls in clusterings:
        print(cls.points)
    return changed


def recomputemeans(clusterings, coords):
    print("\n New Means:")
    for clster in clusterings:
        totalcoord = [0] * len(clusterings)
        for pointer in clster.points:
            for rownum in range(len(clusterings)):
                totalcoord[rownum] += coords[rownum][pointer]
        divisor = float(len(coords[0]))
        newmean = [x / divisor for x in totalcoord]

        clster.mean = newmean
        print(newmean)


def euclidean(point1, point2):
    totaltemp = 0
    for i3 in range(len(point1)):
        totaltemp += abs(point1[i3] - point2[i3]) ** 2
    return math.sqrt(totaltemp)

def matplot():
    print(1)


colors = ['r', 'g', 'b']

fig = plt.figure()

ax = fig.add_subplot(111, projection='3d')

threshold = 0.01

maxiterations = 100

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

print("\nPoints Assigned to Each Cluster: ")

for clusterers in range(len(Clusterings)):
    print(Clusterings[clusterers].points)
    plottingco = [[]]*3
    for pnt in Clusterings[clusterers].points:

        for row in range(k):
            plottingco[row].append(coordData[row][pnt])

    ax.scatter(plottingco[0], plottingco[1], plottingco[2], c=colors[clusterers], marker='o')
    ax.scatter(Clusterings[clusterers].mean[0], Clusterings[clusterers].mean[1],
               Clusterings[clusterers].mean[2], c=colors[clusterers], marker='x')


ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()

changed = sys.maxsize

iterations = 0
# changed > int((len(coordData[0]) * threshold)) or iterations > maxiterations
while changed > 0:
    recomputemeans(Clusterings, coordData)

    changed = reassigncentroids(Clusterings, coordData, k)

    iterations += 1

#
# recomputemeans(Clusterings, coordData)
#
# print("\nMeans After Recomputation")
#
# for clst in Clusterings:
#     print(clst.mean)
#
# print(reassigncentroids(Clusterings, coordData, k))
