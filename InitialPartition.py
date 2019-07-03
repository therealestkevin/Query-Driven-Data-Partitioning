import os

print(os.listdir())

f = open("data.txt","r")

initialInt = f.readline()

print(initialInt)

initList = [int(x) for x in initialInt.split(', ')]

print(initList)

j = 0

for i in range(len(initList)-1):
    print(initList)
    if initList[i] < initList[len(initList)-1]:
        temp = initList[j]
        initList[j] = initList[i]
        initList[i] = temp
        j += 1

temp = initList[int(len(initList)/2)]

initList[int(len(initList)/2)] = initList[len(initList)-1]

initList[len(initList)-1] = temp

print("\nFinal:"+ str(initList))

