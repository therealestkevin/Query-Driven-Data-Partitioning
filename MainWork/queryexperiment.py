from pyclustering.cluster.kmeans import kmeans, kmeans_visualizer
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
from pyclustering.utils import read_sample
from pyclustering.utils.metric import type_metric, distance_metric
from pyclustering.cluster.elbow import elbow
import matplotlib.pyplot as plt
import numpy as np
import math
import sys
from scipy.spatial import distance
import argparse
import os
import random

parser = argparse.ArgumentParser(description="Cluster Characteristic Matrix")
parser.add_argument('-f', '--file', type=str, default="TestData/formatted.txt", help="Text File For Characteristic Matrix Coordinates")

cli = parser.parse_args()


# Intakes Array and Calculates Total Error
# Error in this case being total 0s between first and last 1
def calcError(arr):
    error = 0
    for row in arr:
        endPoint = len(arr[0]) - 1
        startPoint = 0
        endFlag = False
        startFlag = False
        valid = True
        # Finding Last 1
        while not endFlag:
            if row[endPoint] == 1:
                endFlag = True
            elif endPoint == 0:
                endFlag = True
                valid = False
            else:
                endPoint -= 1
        # Find First 1
        while not startFlag:

            if row[startPoint] == 1:
                startFlag = True
            elif startPoint == len(arr[0]) - 1:
                startFlag = True
                valid = False
            else:
                startPoint += 1
        # If 1 was not found in the whole row
        # Simply don't do anything because error is 0 on the row
        if valid:
            for point in range(startPoint, endPoint + 1):
                if row[point] == 0:
                    error += 1
    return error


# Subclustering - Clustering the Clusters
def subcluster(dataset):
    kmin = 1
    kmax = len(dataset)
    optimal_clusters = 1
    # Determining Clusters
    # Might potentially be inefficient technique
    # Instead of elbow, could again repeat what is done
    # in the main clustering, going through K values
    # Choosing one with lowest error from calcError
    # This could be very time intensive however
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


# Main K-Means function
# Takes into data points as well as K value
def runkmeans(sample, clustnum, uniquenum):
    global minError
    global defError

    initial_centers = kmeans_plusplus_initializer(sample, clustnum).initialize()

    # user_function = lambda point1, point2: sum(l1 != 12 for l1, l2 in zip(point1, point2))

    user_function = lambda point1, point2: np.count_nonzero(np.array(point1) != np.array(point2))

    metricUser = distance_metric(type_metric.USER_DEFINED, func=user_function)

    metric = distance_metric(type_metric.EUCLIDEAN)

    kmeans_instance = kmeans(sample, initial_centers, metric=metric)

    kmeans_instance.process()
    clusters = kmeans_instance.get_clusters()


    origMulitDimen = np.array(sample, dtype=int)
    # Data read from text file is coordinates for row
    # Must be transposed in order to obtain proper
    # characteristic matrix
    numpyChar = np.transpose(origMulitDimen)

    mockDataArr = []
    # Column Number Tracking
    for p in range(len(sample)):
        mockDataArr.append(p)
    # Column Position Dictionary
    mockDataPos = {}
    for l in range(len(sample)):
        mockDataPos[l] = l
    # Clusters
    mockDataClustered = []
    # Clusters with Subclusters
    realmockdata = []

    origclustercount = len(clusters)
    # How many times subclustering will happen
    # Log 10 of Total Coord Points
    inception = int(math.log10(len(sample)))
    for num in range(inception):
        for part in clusters:
            newsubclustered = []
            for col in part:
                # Obtaining Cluster
                newsubclustered.append(origMulitDimen[col])
            if len(newsubclustered) > 0:
                # Retrieving Subclusters
                neworder = subcluster(newsubclustered)
                for b in range(len(neworder)):
                    for f in range(len(neworder[b])):
                        neworder[b][f] = part[neworder[b][f]]
                realmockdata.extend(neworder)
                if num == inception - 1:
                    # Appending to Final Cluster Order
                    mockDataClustered.append(neworder)
        # Resetting in case of next subclustering
        clusters = realmockdata.copy()
        realmockdata = []
    # Tracking each Original Cluster
    supercluster = []
    for i in range(len(mockDataClustered)):
        supercluster.append(i)
    # Superclustering based on edges
    # Current simplistic method is taking first
    # Cluster and iterating through, finding
    # which next cluster's left edge matches
    # best to the current clusters right edge
    for i in range(0, len(mockDataClustered) - 1):
        closest = supercluster[i + 1]
        didchange = closest
        closestidx = i + 1
        mindist = sys.maxsize
        # Iterating with both value and index
        for idx, k in enumerate(supercluster[i + 1:]):
            randomsub = random.choice(mockDataClustered[idx + i + 1])
            randomcol = random.choice(randomsub)
            # Calculate Euclidean Distance
            curdist = distance.euclidean(sample[(mockDataClustered[i][len(mockDataClustered[i]) - 1][
                len(mockDataClustered[i][len(mockDataClustered[i]) - 1]) - 1])],
                                         sample[randomcol])
            if curdist < mindist:
                mindist = curdist
                closest = k
                closestidx = idx + i + 1

        if didchange != closest:
            # Swap
            temp = supercluster[i + 1]
            supercluster[i + 1] = closest
            supercluster[closestidx] = temp

    supermockdata = []
    # Compiling Final Clusters
    for i in supercluster:
        supermockdata.append(mockDataClustered[i])
    # Flattening Cluster Nested Arrays
    for k in supermockdata:
        for f in k:
            realmockdata.extend(f)


    originalSave = np.copy(numpyChar)


    # Swapping Actual Characteristic Array
    for i in range(len(mockDataArr) - 1):

        # Checking if current position matches with the ideal value that should be there
        if i != mockDataPos[realmockdata[i]]:
            # Recording Swaps

            # Swapping column number array and actual characteristic matrix columns
            temp = np.copy(numpyChar[:, i])

            realTemp = mockDataArr[i]

            mockDataArr[i] = mockDataArr[mockDataPos[realmockdata[i]]]

            mockDataArr[mockDataPos[realmockdata[i]]] = realTemp

            numpyChar[:, i] = numpyChar[:, mockDataPos[realmockdata[i]]]

            numpyChar[:, mockDataPos[realmockdata[i]]] = temp

            temp2 = mockDataPos[realmockdata[i]]
            # Updating Positions
            mockDataPos[realmockdata[i]] = i

            mockDataPos[realTemp] = temp2





    # Calculating Error
    swappederror = calcError(numpyChar)
    defaulterror = calcError(originalSave)
    defError = defaulterror
    subclusts = 0
    for clust in mockDataClustered:
        subclusts += len(clust)
    # If error is below previously recorded low,
    # Show the visual and save it to image
    if swappederror < minError:

        # fig, ax = plt.subplots(1, 2, figsize=(12, 15.5))
        # clusteredcoltext = " "
        # mid = int(len(mockDataClustered) / 2)

        # Convert subclusters to strings
        # clusteredcoltext += str(supermockdata[:mid])
        # clusteredcoltext += "\n"
        # clusteredcoltext += str(supermockdata[mid:])

        # fig.text(.5, .05, 'Clustered Columns: ' + str(supermockdata), ha='center', wrap=True)
        # f = open("clusters.txt", "w+")
        # f.write(str(supermockdata))
        # fig.text(.5, .1, 'Original Error: ' + str(defaulterror), ha='center')
        # fig.text(.5, .12, 'Clustered Error: ' + str(swappederror), ha='center')
        # fig.suptitle('Sub-Clusters: ' + str(subclusts) +
        #              '  Original Cluster Count: ' + str(origclustercount), fontsize=20)
        # Show black and white representations of characteristic matrix
        # ax[0].imshow(numpyChar, interpolation='nearest', cmap=plt.cm.Greys)
        #
        # ax[1].imshow(originalSave, interpolation='nearest', cmap=plt.cm.Greys)
        #
        # ax[0].title.set_text('Clustered Characteristic Matrix')
        #
        # ax[1].title.set_text('Original Charecteristic Matrix')

        minError = swappederror
        # Save New Low Error Run
        # plt.savefig("TestData/QueryBehaviorVisuals/" + str(uniquenum) + ".png", dpi=130)
        # plt.show()


# Read data from text file

os.chdir('..')
direct = cli.file
name = os.path.join("TestData/PercentData/percents.txt")
f = open(name, "w+")
percents = []
for i in range(1, 200):
    print(str(i) + "\n")
    smp = read_sample("TestData/QueryBehaviorText/" + str(i) + ".txt")
    # Initialize Int maxvalue as error
    defError = 0
    minError = sys.maxsize
    # Getting KMax
    maxCluster = len(smp)
    # Iterating through runs finding lowest error run
    for v in range(1, 50):
        if minError == 0:
            continue

        runkmeans(smp, v, i)
    f.write(str(minError) + " " + str(defError) + "\n")
    percents.append((minError/defError)*100)

f.write("Percents: ")
for percent in percents:
    f.write(str(percent) + "\n")

f.close()
