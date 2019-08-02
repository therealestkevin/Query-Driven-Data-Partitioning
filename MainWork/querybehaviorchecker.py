from pyclustering.cluster.kmeans import kmeans, kmeans_visualizer
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
from pyclustering.samples.definitions import FCPS_SAMPLES
from pyclustering.utils import read_sample
from pyclustering.utils.metric import type_metric, distance_metric
from pyclustering.cluster.elbow import elbow
# from pyclustering.cluster import cluster_visualizer_multidim
import matplotlib.pyplot as plt
import numpy as np
import os


def calcError(arr):
    error = 0
    for row in arr:
        endPoint = len(arr[0])-1
        startPoint = 0
        endFlag = False
        startFlag = False
        while not endFlag:
            if row[endPoint] == 1:
                endFlag = True
            else:
                endPoint -= 1
        while not startFlag:
            if row[startPoint] == 1:
                startFlag = True
            else:
                startPoint += 1
        for point in range(startPoint, endPoint+1):
            if row[point] == 0:
                error += 1
    return error


def createvisual(fileNum, type):
    sample = read_sample("TestData/QueryBehaviorText/"+str(fileNum)+".txt")

    # Sample is simply matrix holding values, can be accessed for values just like any other
    kmin, kmax = 1, len(sample)


    elbow_inst = elbow(sample, kmin, kmax)

    elbow_inst.process()

    optimal_clusters = elbow_inst.get_amount()

    initial_centers = kmeans_plusplus_initializer(sample, optimal_clusters).initialize()

    # user_function = lambda point1, point2: sum(l1 != 12 for l1, l2 in zip(point1, point2))

    user_function = lambda point1, point2: np.count_nonzero(np.array(point1) != np.array(point2))

    metricUser = distance_metric(type_metric.USER_DEFINED, func=user_function)

    # print(metricUser([0, 1, 1], [0, 0, 1]))

    metric = distance_metric(type_metric.EUCLIDEAN)
    if type == 0:
        metric = distance_metric(type_metric.USER_DEFINED, func=user_function)
    kmeans_instance = kmeans(sample, initial_centers, metric=metric)


    kmeans_instance.process()
    clusters = kmeans_instance.get_clusters()
    print(fileNum)
    print(clusters)
    print("\n\n\n")

    final_centers = kmeans_instance.get_centers()

    mockDataArr = []

    for i in range(len(sample)):
        mockDataArr.append(i)
    mockDataPos = {}
    for i in range(len(sample)):
        mockDataPos[i] = i
    # print("\n")
    # print("Position Mapping Hashmap: ", mockDataPos)
    # print("\n")
    # print("Initial Column Positions: ", mockDataArr, "\n")

    mockDataClustered = []

    for cluster in clusters:
        mockDataClustered.extend(cluster)

    imageData = []


    origMulitDimen = np.array(sample, dtype=int)

    # print("Original Coordinates")

    # print(origMulitDimen)

    numpyChar = np.transpose(origMulitDimen)

    originalSave = np.copy(numpyChar)


    printNumpy = np.insert(numpyChar, 0, mockDataArr, 0)

    for i in range(len(mockDataArr) - 1):
        if i != mockDataPos[mockDataClustered[i]]:
            temp = np.copy(numpyChar[:, i])

            realTemp = mockDataArr[i]

            mockDataArr[i] = mockDataArr[mockDataPos[mockDataClustered[i]]]

            mockDataArr[mockDataPos[mockDataClustered[i]]] = realTemp

            numpyChar[:, i] = numpyChar[:, mockDataPos[mockDataClustered[i]]]

            numpyChar[:, mockDataPos[mockDataClustered[i]]] = temp

            temp2 = mockDataPos[mockDataClustered[i]]

            mockDataPos[mockDataClustered[i]] = i

            mockDataPos[realTemp] = temp2


    printArray = np.insert(numpyChar, 0, np.array(mockDataArr), 0)

    swappederror = calcError(numpyChar)
    defaulterror = calcError(originalSave)
    f.write(str(swappederror/defaulterror * 100)+"\n")
    print(swappederror/defaulterror)
    fig, ax = plt.subplots(1, 2)
    fig.suptitle('Clusters: ' + str(len(clusters)), fontsize=20)
    fig.text(.5, .05, 'Clustered Columns: ' + str(clusters), ha='center')
    fig.text(.5, .1, 'Original Error: ' + str(defaulterror), ha='center')
    fig.text(.5, .15, 'Clustered Error: ' + str(swappederror), ha='center')
    ax[0].imshow(numpyChar, cmap=plt.cm.Greys)

    ax[1].imshow(originalSave, cmap=plt.cm.Greys)

    ax[0].title.set_text('Clustered Characteristic Matrix')

    ax[1].title.set_text('Original Charecteristic Matrix')
    fig.set_size_inches(10, 7)
    if type == 0:
        plt.savefig("TestData/QueryBehaviorVisualsHamming/" + str(fileNum) + ".png")
    else:
        plt.savefig("TestData/QueryBehaviorVisualsEuclidean/" + str(fileNum) + ".png")


os.chdir("..")
name = os.path.join("TestData/PercentData/percents.txt")
f = open(name, "w+")

for i in range(3, 20):
    createvisual(i, 1)
f.close()

