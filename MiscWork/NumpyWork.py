import numpy

numpTest =numpy.array([[1, 0, 0],
                       [0, 1, 1],
                       [1, 1, 0]])

temp = numpy.copy(numpTest[:, 1])

numpTest[:, 1] = numpTest[:, 2]

numpTest[:, 2] = temp

print(numpTest)