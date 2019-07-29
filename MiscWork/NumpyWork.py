import numpy
from pyclustering.cluster.kmeans import kmeans, kmeans_visualizer
from pyclustering.cluster.center_initializer import kmeans_plusplus_initializer

numpTest =numpy.array([[1, 0, 0],
                       [0, 1, 1],
                       [1, 1, 0]])

temp = numpy.copy(numpTest[:, 1])

numpTest[:, 1] = numpTest[:, 2]

numpTest[:, 2] = temp

print(numpTest)

testlist = [[[3, 2], [4, 2]], [[2, 3], [7, 8]]]

testlist.remove([[3, 2], [4, 2]])

print(testlist)

initial_centers = kmeans_plusplus_initializer(numpTest, 3).initialize()
kmeans_instance = kmeans(numpTest, initial_centers)
kmeans_instance.process()
clusters = kmeans_instance.get_clusters()
print(clusters)
