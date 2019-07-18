from pyclustering.cluster.kmeans import kmeans, kmeans_visualizer
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
from pyclustering.utils import read_sample
from pyclustering.utils.metric import type_metric, distance_metric
from pyclustering.cluster.elbow import elbow
import matplotlib.pyplot as plt
import numpy as np
import time
import math
import copy
import sys
from scipy.spatial import distance

def calcError(arr):
    error = 0
    for row in arr:
        endPoint = len(arr[0])-1
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
            elif startPoint == len(arr)-1:
                startFlag = True
                valid = False
            else:
                startPoint += 1
        if valid:
            for point in range(startPoint, endPoint+1):
                if row[point] == 0:
                    error += 1
    return error


def subcluster(dataset):

    kmin = len(dataset[0])
    kmax = len(dataset)
    optimal_clusters = 1
    if kmax - kmin <= 3:
        optimal_clusters = int((kmin+kmax)/2)
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
    t0 = time.time()
    # kmin, kmax = int(len(sample[0])/2), len(sample)
    #
    # elbow_inst = elbow(sample, kmin, kmax)
    #
    # elbow_inst.process()
    #
    # optimal_clusters = elbow_inst.get_amount()
    # print("Optimal K Clusters: ", optimal_clusters)

    initial_centers = kmeans_plusplus_initializer(sample, clustnum).initialize()

    # user_function = lambda point1, point2: sum(l1 != 12 for l1, l2 in zip(point1, point2))

    user_function = lambda point1, point2: np.count_nonzero(np.array(point1) != np.array(point2))

    metricUser = distance_metric(type_metric.USER_DEFINED, func=user_function)

    metric = distance_metric(type_metric.EUCLIDEAN)

    kmeans_instance = kmeans(sample, initial_centers, metric=metric)
    print("Centroids: ", kmeans_instance.get_centers())

    kmeans_instance.process()
    origclusters = kmeans_instance.get_clusters()
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
                    mockDataClustered.append(neworder)
            # elif len(newsubclustered) == 1:
            #     realmockdata.append(part)
        clusters = realmockdata.copy()
        realmockdata = []
    imageData = []
    supercluster = []
    for i in range(len(mockDataClustered)):
        supercluster.append(i)
    for i in range(0, len(mockDataClustered)-1):
        closest = supercluster[i+1]
        didchange = closest
        closestidx = i + 1
        mindist = sys.maxsize
        for idx, k in enumerate(supercluster[i+1:]):
            curdist = distance.euclidean(sample[(mockDataClustered[i][len(mockDataClustered[i])-1][len(mockDataClustered[i][len(mockDataClustered[i])-1])-1])],
                                     sample[mockDataClustered[idx+i+1][0][0]])
            if curdist < mindist:
                mindist = curdist
                closest = k
                closestidx = idx + i + 1
        if didchange == closest:
            print("Nothing Happened")
        else:
            temp = supercluster[i+1]
            supercluster[i+1] = closest
            supercluster[closestidx] = temp
    supermockdata = []
    for i in supercluster:
        supermockdata.append(mockDataClustered[i])
    for k in supermockdata:
        for f in k:
            realmockdata.extend(f)
    print("L: ", realmockdata)
    print("M: ", mockDataArr, "\n")

    originalSave = np.copy(numpyChar)

    print("Characteristic Matrix (First Row is Column Numbers)")
    printNumpy = np.insert(numpyChar, 0, mockDataArr, 0)
    print(printNumpy, "\n")
    for i in range(len(mockDataArr)-1):
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
    t1 = time.time()

    print("\n\nColumn Positions After Swapping: ", mockDataArr)


    print("\n\nFinal Swapped Characteristic Matrix (First Row is Column Numbers)")
    printArray = np.insert(numpyChar, 0, np.array(mockDataArr), 0)

    print(printArray)

    swappederror = calcError(numpyChar)
    defaulterror = calcError(originalSave)
    subclusts = 0
    for clust in mockDataClustered:
        subclusts += len(clust)
    if swappederror < minError:
        print("\n\nTotal Runtime: ", (t1 - t0))
        fig, ax = plt.subplots(1, 2)
        clusteredcoltext = " "
        mid = int(len(mockDataClustered) / 2)
        clusteredcoltext += str(supermockdata[:mid])
        clusteredcoltext += "\n"
        clusteredcoltext += str(supermockdata[mid:])

        fig.text(.5, .05, 'Clustered Columns: ' + str(clusteredcoltext), ha='center')
        f = open("clusters.txt", "w+")
        f.write(str(supermockdata))
        fig.text(.5, .125, 'Original Error: ' + str(defaulterror), ha='center')
        fig.text(.5, .15, 'Clustered Error: ' + str(swappederror), ha='center')
        fig.suptitle('Sub-Clusters: ' + str(subclusts) +
                     '  Original Cluster Count: ' + str(origclustercount), fontsize=20)

        ax[0].imshow(numpyChar, interpolation='none', cmap=plt.cm.Greys)

        ax[1].imshow(originalSave, interpolation='none', cmap=plt.cm.Greys)

        ax[0].title.set_text('Clustered Characteristic Matrix')

        ax[1].title.set_text('Original Charecteristic Matrix')

        minError = swappederror
        plt.savefig("Winner.png", dpi=130)
        plt.show()


sample = read_sample("TestData/formatted.txt")

minError = 100000000000000000000000

maxCluster = len(sample)

for v in range(1, maxCluster):
    print(v)
    runkmeans(sample, v)
