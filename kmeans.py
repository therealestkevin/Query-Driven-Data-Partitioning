from pyclustering.cluster.kmeans import kmeans, kmeans_visualizer
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
from pyclustering.samples.definitions import FCPS_SAMPLES
from pyclustering.utils import read_sample
from pyclustering.utils.metric import type_metric, distance_metric
from pyclustering.cluster.elbow import elbow
# from pyclustering.cluster import cluster_visualizer_multidim
import matplotlib.pyplot as plt
import numpy as np
import time

# sample = read_sample(FCPS_SAMPLES.SAMPLE_WING_NUT)
t0 = time.time()
sample = read_sample("TestData/bitvector.txt")

# Sample is simply matrix holding values, can be accessed for values just like any other
kmin, kmax = len(sample[0]), len(sample[0])*4

elbow_inst = elbow(sample, kmin, kmax)

elbow_inst.process()

optimal_clusters = elbow_inst.get_amount()
print("Optimal K Clusters: ", optimal_clusters )
initial_centers = kmeans_plusplus_initializer(sample, optimal_clusters).initialize()

# user_function = lambda point1, point2: sum(l1 != 12 for l1, l2 in zip(point1, point2))

user_function = lambda point1, point2: np.count_nonzero(np.array(point1) != np.array(point2))

metricUser = distance_metric(type_metric.USER_DEFINED, func=user_function)

# print(metricUser([0, 1, 1], [0, 0, 1]))

metric = distance_metric(type_metric.EUCLIDEAN)

kmeans_instance = kmeans(sample, initial_centers, metric=metricUser)
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
# print("\n")
# print("Position Mapping Hashmap: ", mockDataPos)
# print("\n")
# print("Initial Column Positions: ", mockDataArr, "\n")


mockDataClustered = []

for cluster in clusters:
    mockDataClustered.extend(cluster)

imageData = []
print("L: ",mockDataClustered)
print("M: ", mockDataArr, "\n")

"""
For loop below is column swapping 
It is essentially brute force and assumes
an initial arbitrary order of the clusters
that will be ideal basis that the initial positions
will try to adjust to. If a position is not the ideal
that position will be swapped with the ideal column
This is done through a Hashmap that maps positions
of each column in order to ensure that correct swapping
is possible. More efficient techniques will definitely
be more desirable and is something to be explored
"""
origMulitDimen = np.array(sample, dtype=int)

# print("Original Coordinates")

# print(origMulitDimen)

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

print("\n\nTotal Runtime: ", (t1-t0))
fig, ax = plt.subplots(1, 2)

ax[0].imshow(numpyChar, cmap=plt.cm.Greys)

ax[1].imshow(originalSave, cmap=plt.cm.Greys)

ax[0].title.set_text('Clustered Characteristic Matrix')

ax[1].title.set_text('Original Charecteristic Matrix')

plt.show()


# kmeans_visualizer.show_clusters(sample, clusters, final_centers)
