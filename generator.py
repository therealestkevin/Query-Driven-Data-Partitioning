import random as rn
import numpy as np
import argparse

# creating a binary matrix for dim dimensional data set
# dataSetSize points in data set, querySetSize queries
# queries cover up to 20% of the data, data in data set has range data set size
# using seeds for random generation of queries and data set
# approximate run times for default values:  1D: 10 s   2D: 15 s   3D: 20 s

# This program focuses on different kinds of skew for data

# creating command line arguments
parser = argparse.ArgumentParser(description="Generate Binary Matrix")
parser.add_argument('-D', '--Dim', type=int, default=1, help="dimension of data")
parser.add_argument('-x', '--data_seed', type=int, default=1, help="seed for random data")
parser.add_argument('-y', '--query_seed', type=int, default=1, help="seed for random queries")
parser.add_argument('-q', '--query_size', type=int, default=1000, help="number of queries (y axis for binary matrix)")
parser.add_argument('-d', '--data_size', type=int, default=1000000, help="data size (x axis for binary matrix)")
parser.add_argument('-p', '--path', default="binary_matrix_skew.txt", help="file to save matrix")
parser.add_argument('-c', '--max_coverage', type=float, default=.2, help="maximum percentage of data queries can cover")
parser.add_argument('-s', '--skew', type=int, default=0, help="value 0-dim: 0 randomize skew, 1-dim is most/least skew")

args = parser.parse_args()

if not 0 <= args.skew <= args.Dim:
    args.skew = 0  # skew must be between 0 and dim

####
# creating a data set
np.random.seed(args.data_seed)
# each column of numbers in data matrix is a data point
data = np.random.rand(args.Dim, args.data_size)
data *= args.data_size
data = data.astype(int)

####
# each query on average will have a slight bias towards one axis
# each query consists of a range for x and a range for y, written as two sets of numbers
# queries can cover anywhere from a 0 to max_coverage percent of the data points
# skew determines how many axes will have restrictions - eg skew = 1 means that only one axis has a value != 1
# when skew = 0, queries will have skews randomly assigned

rn.seed(args.query_seed)
query_array = np.zeros((args.query_size, args.Dim, 2), dtype=np.uint32)

percent = np.ones(args.Dim)
skew = args.skew - 1
for q in query_array:
    if args.skew == 0:
        skew = rn.randint(0, args.Dim - 1)
    total_percent = rn.uniform(0, args.max_coverage)  # picking a percent of the total data for this specific query
    # generating percents along each axis with product total_percent
    for p in range(skew):  # only goes into effect for skew >= 2
        percent[p] = rn.uniform(total_percent / np.prod(percent), 1)  # avoiding percentages > 1
    percent[skew] = total_percent / np.prod(percent)
    percent *= args.data_size  # range of query axes
    # choosing random int to represent favored axis for query
    favored_axis = rn.randint(0, args.Dim - 1)
    for index in range(args.Dim):
        axis_percent = int(percent[(index + favored_axis) % args.Dim])
        q[index][0] = rn.randint(0, (args.data_size - axis_percent))  # lower bound
        q[index][1] = q[index][0] + axis_percent + 1  # upper bound, will round to nearest whole number
    # resetting percent values
    percent.fill(1)

####
# creating a binary matrix -- 1 for if query is valid on data, 0 if no
binary_matrix = np.zeros((args.query_size, args.data_size), dtype=np.uint8)
axes_matrix = np.ones((args.Dim, args.data_size), dtype=bool)

i = 0
for query in query_array:
    # axes_matrix[j] represents point validity along axis j
    for j in range(args.Dim):
        if query[j][0] != 0 or query[j][1] != (args.data_size + 1):  # don't need to calc if cover 100% data
            axes_matrix[j] = np.logical_and(data[j] >= query[j][0], data[j] < query[j][1])
    # creating valid matrix of whether point satisfies query
    valid = axes_matrix[0]
    for k in range(1, args.Dim):  # cycling through axes
        valid = np.logical_and(valid, axes_matrix[k])
    # if a point is valid, its value should be changed to 1
    binary_matrix[i][valid] = 1
    i += 1

print(binary_matrix)

np.savetxt(args.path, binary_matrix, fmt='%i', delimiter="")  # takes some minutes to save for default values



