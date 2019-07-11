from pyclustering.cluster.kmeans import kmeans, kmeans_visualizer
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer
from pyclustering.samples.definitions import FCPS_SAMPLES
from pyclustering.utils import read_sample
from pyclustering.utils.metric import type_metric, distance_metric
from pyclustering.cluster.elbow import elbow
# from pyclustering.cluster import cluster_visualizer_multidim
import numpy as np

# sample = read_sample(FCPS_SAMPLES.SAMPLE_WING_NUT)
sample = read_sample("bitvector.txt")

kmin, kmax = 2, 10

elbow_inst = elbow(sample, kmin, kmax)

elbow_inst.process()

optimal_clusters = elbow_inst.get_amount()

initial_centers = kmeans_plusplus_initializer(sample, optimal_clusters).initialize()

# user_function = lambda point1, point2: sum(l1 != 12 for l1, l2 in zip(point1, point2))

user_function = lambda point1, point2: np.count_nonzero(np.array(point1) != np.array(point2))

metricUser = distance_metric(type_metric.USER_DEFINED, func=user_function)

# print(metricUser([0, 1, 1], [0, 0, 1]))

metric = distance_metric(type_metric.EUCLIDEAN)

kmeans_instance = kmeans(sample, initial_centers, metric=metric)

kmeans_instance.process()
clusters = kmeans_instance.get_clusters()
final_centers = kmeans_instance.get_centers()

print("Resulting Clusters ", clusters)

print("SSE: ", kmeans_instance.get_total_wce())

mockDataArr = []

for i in range(len(sample)):
    mockDataArr.append(i)
mockDataPos = {}
for i in range(len(sample)):
    mockDataPos[i] = i
print("\n")
print("Position Mappings: ", mockDataPos)
print("\n")
print("Initial Column Positions: ", mockDataArr)
print("\n")

mockDataClustered = []

for cluster in clusters:
    mockDataClustered.extend(cluster)

for i in range(len(mockDataArr)-1):
    if mockDataArr[i] != mockDataClustered[i]:
        print("Index: " + str(i) + "    Value: " + str(mockDataArr[i]) + "  Swaps With -> " + "Index: "
              + str(mockDataPos[mockDataClustered[i]]) + "  Value: " + str(mockDataArr[mockDataPos[mockDataClustered[i]]]))

        temp = mockDataArr[i]
        mockDataArr[i] = mockDataArr[mockDataPos[mockDataClustered[i]]]
        mockDataArr[mockDataPos[mockDataClustered[i]]] = temp
        temp2 = mockDataPos[mockDataClustered[i]]
        mockDataPos[mockDataClustered[i]] = i
        mockDataPos[temp] = temp2


print("\n\nResult After Swapping"+str(mockDataArr))


kmeans_visualizer.show_clusters(sample, clusters, final_centers)
