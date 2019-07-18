import numpy as np
import os


def split(word):
    return [char for char in word]


filename = os.path.join("TestData/largerealset.txt")
f = open(filename, "r")
data = f.readlines()
matrix = np.array([], int)
matrix = np.hstack([matrix, list(map(int, split(data[0])[:len(split(data[0]))-1]))])
print(matrix)
for i in range(1, len(data)):
    curLine = data[i]
    curChars = split(curLine)
    if i == len(data) -1:
        curInts = list(map(int, curChars))
    else:
        curInts = list(map(int, curChars[: len(curChars)-1]))
    matrix = np.vstack([matrix, np.array(curInts)])

matrix = matrix.transpose()

printname = os.path.join("TestData/formatted.txt")
f2 = open(printname, "w+")

for i in matrix:

    for j in i:
        f2.write(str(j) + " ")

    f2.write("\n")

f2.close()

