from pyclustering.cluster.kmeans import kmeans, kmeans_visualizer
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
from pyclustering.utils import read_sample
from pyclustering.utils.metric import type_metric, distance_metric
from pyclustering.cluster.elbow import elbow
import matplotlib.pyplot as plt
import numpy as np
import math
import os
import argparse

parser = argparse.ArgumentParser(description="Cluster Characteristic Matrix")
parser.add_argument('-f', '--file', type=str, default="TestData/formatted.txt", help="Text File For Characteristic Matrix Coordinates")

cli = parser.parse_args()

def calcError(arr):
    error = 0
    for row in arr:
        endPoint = len(arr[0]) - 1
        startPoint = 0
        endFlag = False
        startFlag = False
        valid = True
        while not endFlag:
            if row[endPoint] == 1:
                endFlag = True
            elif endPoint == 0:
                endFlag = True
                valid = False
            else:
                endPoint -= 1
        while not startFlag:

            if row[startPoint] == 1:
                startFlag = True
            elif startPoint == len(arr[0]) - 1:
                startFlag = True
                valid = False
            else:
                startPoint += 1
        if valid:
            for point in range(startPoint, endPoint + 1):
                if row[point] == 0:
                    error += 1
    return error


def reorder(ideal, original):
    print()


def subcluster(dataset):
    kmin = len(dataset[0])
    kmax = len(dataset)
    optimal_clusters = 1
    if kmax - kmin <= 3:
        optimal_clusters = int((kmin + kmax) / 2)
    else:
        elbow_inst = elbow(dataset, kmin, kmax)
        elbow_inst.process()
        optimal_clusters = elbow_inst.get_amount()
    if optimal_clusters > len(dataset):
        optimal_clusters = len(dataset)
    initial_centers = kmeans_plusplus_initializer(dataset, optimal_clusters).initialize()
    metric = distance_metric(type_metric.EUCLIDEAN)
    kmeans_instance = kmeans(dataset, initial_centers, metric=metric)
    kmeans_instance.process()
    clusters = kmeans_instance.get_clusters()

    return clusters


def runkmeans(sample, clustnum):
    global minError

    initial_centers = kmeans_plusplus_initializer(sample, clustnum).initialize()

    # user_function = lambda point1, point2: sum(l1 != 12 for l1, l2 in zip(point1, point2))

    user_function = lambda point1, point2: np.count_nonzero(np.array(point1) != np.array(point2))

    metricUser = distance_metric(type_metric.USER_DEFINED, func=user_function)

    metric = distance_metric(type_metric.EUCLIDEAN)

    kmeans_instance = kmeans(sample, initial_centers, metric=metric)
    print("Centroids: ", kmeans_instance.get_centers())

    kmeans_instance.process()
    clusters = kmeans_instance.get_clusters()

    print("Output Clusters", clusters)
    final_centers = kmeans_instance.get_centers()

    print("Centroids: ", kmeans_instance.get_centers())

    print("SSE: ", kmeans_instance.get_total_wce())

    origMulitDimen = np.array(sample, dtype=int)

    numpyChar = np.transpose(origMulitDimen)

    mockDataArr = []

    for p in range(len(sample)):
        mockDataArr.append(p)
    mockDataPos = {}
    for l in range(len(sample)):
        mockDataPos[l] = l

    mockDataClustered = []

    realmockdata = []
    origclustercount = len(clusters)
    inception = int(math.log10(len(sample)))
    for num in range(inception):
        for part in clusters:

            newsubclustered = []
            for col in part:
                newsubclustered.append(origMulitDimen[col])

            if len(newsubclustered) > 0:
                neworder = subcluster(newsubclustered)

                for b in range(len(neworder)):
                    for f in range(len(neworder[b])):
                        neworder[b][f] = part[neworder[b][f]]
                realmockdata.extend(neworder)
                if num == inception - 1:
                    mockDataClustered.extend(neworder)
            # elif len(newsubclustered) == 1:
            #     realmockdata.append(part)
        clusters = realmockdata.copy()
        realmockdata = []
    imageData = []

    for k in mockDataClustered:
        realmockdata.extend(k)
    print("L: ", realmockdata)
    print("M: ", mockDataArr, "\n")

    originalSave = np.copy(numpyChar)

    print("Characteristic Matrix (First Row is Column Numbers)")
    printNumpy = np.insert(numpyChar, 0, mockDataArr, 0)
    print(printNumpy, "\n")
    for i in range(len(mockDataArr) - 1):
        print("I: " + str(i))
        print("RealMockData: ", realmockdata)
        print("Length: ", len(realmockdata))
        if i != mockDataPos[realmockdata[i]]:
            print("Index: " + str(i) + "    Value: " + str(numpyChar[:, i]) + "  Swaps With -> " + "Index: "
                  + str(mockDataPos[realmockdata[i]]) + "  Value: " + str(numpyChar[:, mockDataPos[realmockdata[i]]]))

            temp = np.copy(numpyChar[:, i])

            realTemp = mockDataArr[i]

            mockDataArr[i] = mockDataArr[mockDataPos[realmockdata[i]]]

            mockDataArr[mockDataPos[realmockdata[i]]] = realTemp

            numpyChar[:, i] = numpyChar[:, mockDataPos[realmockdata[i]]]

            numpyChar[:, mockDataPos[realmockdata[i]]] = temp

            temp2 = mockDataPos[realmockdata[i]]

            mockDataPos[realmockdata[i]] = i

            mockDataPos[realTemp] = temp2

    print("\n\nColumn Positions After Swapping: ", mockDataArr)

    print("\n\nFinal Swapped Characteristic Matrix (First Row is Column Numbers)")
    printArray = np.insert(numpyChar, 0, np.array(mockDataArr), 0)

    print(printArray)

    swappederror = calcError(numpyChar)
    defaulterror = calcError(originalSave)

    if swappederror < minError:
        fig, ax = plt.subplots(1, 2)
        clusteredcoltext = " "
        mid = int(len(mockDataClustered) / 2)
        clusteredcoltext += str(mockDataClustered[:mid])
        clusteredcoltext += "\n"
        clusteredcoltext += str(mockDataClustered[mid:])

        fig.text(.5, .05, 'Clustered Columns: ' + str(clusteredcoltext), ha='center')
        f = open("clusters.txt", "w+")
        f.write(str(mockDataClustered))
        fig.text(.5, .15, 'Original Error: ' + str(defaulterror), ha='center')
        fig.text(.5, .2, 'Clustered Error: ' + str(swappederror), ha='center')
        fig.suptitle('Sub-Clusters: ' + str(len(mockDataClustered)) +
                     '  Original Cluster Count: ' + str(origclustercount), fontsize=20)

        ax[0].imshow(numpyChar, interpolation='none', cmap=plt.cm.Greys)

        ax[1].imshow(originalSave, interpolation='none', cmap=plt.cm.Greys)

        ax[0].title.set_text('Clustered Characteristic Matrix')

        ax[1].title.set_text('Original Charecteristic Matrix')

        minError = swappederror
        plt.savefig("Winner.png", dpi=130)
        # plt.show()


os.chdir('..')
direct = cli.file
smp = read_sample(direct)

minError = 100000000000000000000000

maxCluster = len(smp)

for v in range(6, maxCluster):
    print(v)
    runkmeans(smp, v)
