# RISE 2019 Query Driven Data Partitioning

This repository contains work mainly pertaining to clustering and visualization processes regarding this project.

The clustering is conducted through the Python library PyClustering: https://github.com/annoviko/pyclustering

PyClustering is a collection of various data mining techniques. Regarding Clustering Algorithms, there is a lot of  
flexibility in the algorithm you want to use. With regards to K-Means, there is a lot of adaptability with distances.  
Instead of being confined to Euclidean, there are options to create user defined distances which allow ease of use with  
other distances such as Hamming:  
  
```
#!python

hamming_distance = lambda point1, point2: np.count_nonzero(np.array(point1) != np.array(point2))

metricHamming = distance_metric(type_metric.USER_DEFINED, func=hamming_distance)
```

Once clusters are returned, the columns of the characteristic matrix are swapped in order to satisfy the clusterings.  
The process through which I do this currently is mostly brute force and improvements to this would be desired.  
I initially create an array ***L*** in which column numbers are assigned to arbitrary column in which they are all  
grouped in their respective clusters. Then, a dictionary mapping each column to its position is made. Finally, an array ***M*** with values [1, 2, ... N] is created with N being column count representing each individual column of the characteristic matrix. ***M*** is sequentially iterated through and if the current index being iterated through is not equal to the current position of the column of the same index within ***L***, then a swap occurs between the current column being iterated and the column that should be there. Positions are then updated. An example of this swapping is shown below.  


![swapping](https://user-images.githubusercontent.com/30887959/61324666-d6778b80-a7c7-11e9-82f8-c5f947dd4763.png)

An image showing an overview of the process of swapping and resulting matrix is shown below.  

![overview](https://user-images.githubusercontent.com/30887959/61324665-d6778b80-a7c7-11e9-8c45-72952caffa93.png)
![visualization](https://user-images.githubusercontent.com/30887959/61324667-d6778b80-a7c7-11e9-947d-44dafcf35c96.png)
Visualizations are all done through matplotlib.  
Results seemed to be mixed so far with K-Means. With PyClustering, clusters are decided beforehand with elbow method.   
With both Euclidean and Hamming distances, some runs produce nice results with 1s placed next to each  
other such as in the visualization above but other runs are often jumbled and seemingly unclustered.  
Problems arise within clusters themselves as like objects are not placed next to each other, creating weird clusterings (See columns 4, 6, 15, etc. in visualization).  
Clusters themselves could be clustered again to solve this issue and is something I am currently working on.  





