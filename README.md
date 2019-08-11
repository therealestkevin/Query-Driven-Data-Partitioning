# Query-Driven Data-Agnostic Data Partitioning

## Background:

• Physical layout of data is essential in ensuring range query efficiency in disk storage

• Data that answer the same query can be collocated to minimize unnecessary accesses

• With one-dimensional (1-D) integer data, reading & sorting data accomplishes this

• Data is often not integer-based and can be multi-dimensional.

• When query access patterns are unpredictable and reading physical data is either not possible or too costly, finding strong data layouts becomes an interesting problem

• Data Mining algorithms, specifically clustering, allow us to develop a possible solution

![image](https://user-images.githubusercontent.com/30887959/62838161-696fde00-bc2d-11e9-97e2-32bd8cfcf1fe.png)

*Comparison of contiguous and non-contiguous access*

## Approach:

• Use query responses and workload access patterns to simplify complex data and form representations of original data

![image](https://user-images.githubusercontent.com/30887959/62838225-19454b80-bc2e-11e9-93c1-84c9488b6e52.png)

*Creating what is called the Characteristic Matrix, a binary matrix representing query access patterns across a workload*

• A column consists of an object’s responses to the whole query workload and signifies common access patterns

• Use columns as coordinate points to represent original data and conduct clustering with Kmeans algorithm (Euclidean distance)

![image](https://user-images.githubusercontent.com/30887959/62838242-5f9aaa80-bc2e-11e9-8ff4-5d935789a765.png)

*Representation of K-means iteration*

• According to the resulting clusters, the Characteristic Matrix is rearranged, placing clustered columns together

• Error metric evaluates clustering effectiveness

![image](https://user-images.githubusercontent.com/30887959/62838251-8b1d9500-bc2e-11e9-9f83-6ff4812b0e1d.png)

*Error function calculating effectiveness of clustering where k is the first occurrence of a 1 in the current row, n is the last
occurrence, and 𝑀 sub 𝑐 is the characteristic matrix. The metric is a physical representation of unnecessary page accesses.*


• Clustering observed in varying data set sizes, query counts, and dimensions
