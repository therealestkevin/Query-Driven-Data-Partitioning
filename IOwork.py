import os

f = open("QueryDrivenDataPartitioning/data.txt","r")

initialInt = f.readline()

print(initialInt)

initList = [int(x) for x in initialInt.split(', ')]

print(initList)

