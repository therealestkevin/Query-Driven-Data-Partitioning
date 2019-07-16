import numpy as np
from kmode.kmodes import KModes
import matplotlib.pyplot as plt

from pyclustering.utils import read_sample

sample = np.array(read_sample("TestData/bitvector.txt"), int)

print(sample)

km = KModes(n_clusters=len(sample[0]), init='Huang', verbose=1)

labels = km.fit_predict(sample)

print(labels)

clusters = [[] for i in range(len(sample[0]))]

print(clusters)

for i in range(len(labels)):
    clusters[labels[i]].append(i)

print(clusters)

mockDataArr = []

for i in range(len(sample)):
    mockDataArr.append(i)

mockDataPos = {}

for i in range(len(sample)):
    mockDataPos[i] = i

print("\n")
print("Position Mapping Hashmap: ", mockDataPos)
print("\n")
print("Initial Column Positions: ", mockDataArr)
print("\n")

mockDataClustered = []

for cluster in clusters:
    mockDataClustered.extend(cluster)

imageData = []

origMulitDimen = np.array(sample, dtype=int)

print("Original Coordinates")

print(origMulitDimen)

numpyChar = np.transpose(origMulitDimen)

originalSave = np.copy(numpyChar)

print("\n\nTransposed Coordinates to Characteristic Matrix")

print(numpyChar, "\n")

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

print("\n\nResult After Swapping: ", mockDataArr)

print("\n\nFinal Swapped Characteristic Matrix")

print(numpyChar)

fig, ax = plt.subplots(1, 2)

ax[0].imshow(numpyChar, cmap=plt.cm.Greys)

ax[1].imshow(originalSave, cmap=plt.cm.Greys)

ax[0].title.set_text('Clustered Characteristic Matrix')

ax[1].title.set_text('Original Charecteristic Matrix')

plt.show()

