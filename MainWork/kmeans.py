from pyclustering.cluster.kmeans import kmeans, kmeans_visualizer
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
from pyclustering.utils import read_sample
from pyclustering.utils.metric import type_metric, distance_metric
from pyclustering.cluster.elbow import elbow
import matplotlib.pyplot as plt
import numpy as np
import time




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


def runkmeans(sample, clustnum):
    global minError
    t0 = time.time()

    # kmin, kmax = len(sample[0]), len(sample[0])*4
    #
    # elbow_inst = elbow(sample, kmin, kmax)
    #
    # elbow_inst.process()
    #
    # optimal_clusters = elbow_inst.get_amount()
    # print("Optimal K Clusters: ", optimal_clusters)

    initial_centers = kmeans_plusplus_initializer(sample, clustnum).initialize()

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

    mockDataArr = []

    for i in range(len(sample)):
        mockDataArr.append(i)
    mockDataPos = {}
    for i in range(len(sample)):
        mockDataPos[i] = i

    mockDataClustered = []

    for cluster in clusters:
        mockDataClustered.extend(cluster)

    imageData = []
    print("L: ",mockDataClustered)
    print("M: ", mockDataArr, "\n")

    origMulitDimen = np.array(sample, dtype=int)

    numpyChar = np.transpose(origMulitDimen)

    originalSave = np.copy(numpyChar)

    print("Characteristic Matrix (First Row is Column Numbers)")
    printNumpy = np.insert(numpyChar, 0, mockDataArr, 0)
    print(printNumpy, "\n")
    for i in range(len(mockDataArr)-1):
        if i != mockDataPos[mockDataClustered[i]]:
            print("Index: " + str(i) + "    Value: " + str(numpyChar[:, i]) + "  Swaps With -> " + "Index: "
                  + str(mockDataPos[mockDataClustered[i]]) + "  Value: " + str(numpyChar[:, mockDataPos[mockDataClustered[i]]]))

            temp = np.copy(numpyChar[:, i])

            realTemp = mockDataArr[i]

            mockDataArr[i] = mockDataArr[mockDataPos[mockDataClustered[i]]]

            mockDataArr[mockDataPos[mockDataClustered[i]]] = realTemp

            numpyChar[:, i] = numpyChar[:, mockDataPos[mockDataClustered[i]]]

            numpyChar[:, mockDataPos[mockDataClustered[i]]] = temp

            temp2 = mockDataPos[mockDataClustered[i]]

            mockDataPos[mockDataClustered[i]] = i

            mockDataPos[realTemp] = temp2
    t1 = time.time()

    print("\n\nColumn Positions After Swapping: ", mockDataArr)

    # swappedCharecteristic = np.array([numpyChar[:, mockDataArr[0]]]).transpose()
    #
    # for num in mockDataArr[1:]:
    #     temp = np.array([numpyChar[:, num]]).transpose()
    #     swappedCharecteristic = np.append(swappedCharecteristic, temp, axis=1)

    print("\n\nFinal Swapped Characteristic Matrix (First Row is Column Numbers)")
    printArray = np.insert(numpyChar, 0, np.array(mockDataArr), 0)

    print(printArray)

    swappederror = calcError(numpyChar)
    defaulterror = calcError(originalSave)

    if swappederror < minError:
        print("\n\nTotal Runtime: ", (t1 - t0))
        fig, ax = plt.subplots(1, 2)
        fig.suptitle('Clusters: ' + str(len(clusters)), fontsize=20)
        fig.text(.5, .05, 'Clustered Columns: ' + str(clusters), ha='center')
        fig.text(.5, .1, 'Original Error: ' + str(defaulterror), ha='center')
        fig.text(.5, .15, 'Clustered Error: ' + str(swappederror), ha='center')
        ax[0].imshow(numpyChar, cmap=plt.cm.Greys)

        ax[1].imshow(originalSave, cmap=plt.cm.Greys)

        ax[0].title.set_text('Clustered Characteristic Matrix')

        ax[1].title.set_text('Original Charecteristic Matrix')

        minError = swappederror
        plt.savefig("Winner.png")






minError = 100000000000000000000000
sample = read_sample("TestData/formatted.txt")
maxCluster = len(sample)

for i in range(1, maxCluster):
    runkmeans(sample, i)
