def partition(arr, start, end):
    j = start

    for i in range(start,end):
        if arr[i] < arr[end - 1]:
            temp = arr[j]
            arr[j] = arr[i]
            arr[i] = temp
            j += 1

    temp = arr[j]

    arr[j] = arr[end-1]

    arr[end - 1] = temp

    print("\nCurrent Partition:" + str(arr))
    return j


def sort(arr, start, end):
    if start < end:
        pivot = partition(arr,start,end)

        sort(arr, start, pivot)
        sort(arr, pivot+1, end)


f = open("data.txt", "r")

initialInt = f.readline()

print("String Read: " + initialInt)

initList = [int(x) for x in initialInt.split(', ')]

print("List Obtained: " + str(initList))

sort(initList, 0, len(initList))

print("\nSorted List: " + str(initList))




