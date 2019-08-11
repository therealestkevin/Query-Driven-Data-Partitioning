# Query-Driven Data-Agnostic Data Partitioning

***My research during my time as a summer 2019 intern in the Boston University Department of Computer Science working under Professor Manos Athanassoulis***

[Poster](https://github.com/therealestkevin/Query-Driven-Data-Partitioning/files/3490406/Xu.Kevin.POSTER.pdf)

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

## Sub-Clustering & Super-Clustering:

• Issue: With the base K-means clustering, the ordering of columns within a cluster is completely numerical, meaning that similar columns within a cluster are not placed together. Moreover, there is no way to physically order the clusters, meaning edges are not matched up and error is greater. This problem is one of both intra-cluster and inter-cluster magnitude. The solutions to these problems are detailed below.

• Sub-Clustering: Clustering the clusters, intra-cluster ordering occurring log10(𝐷) times (D is # data points)

• Super-Clustering: Inter-Cluster ordering by edge column distance

![image](https://user-images.githubusercontent.com/30887959/62838293-054e1980-bc2f-11e9-9b09-9108a03610ca.png)

*Visual comparison of clustering techniques on same 20 object 4 query dataset*

## Results:

![image](https://user-images.githubusercontent.com/30887959/62838325-552ce080-bc2f-11e9-8bde-7bf9fca054ef.png)

*Visual represetnation of an example query workload with clustered and original matrices*

![image](https://user-images.githubusercontent.com/30887959/62838338-7988bd00-bc2f-11e9-9153-86ee0eea3d14.png)

*Percentage and raw error after clustering 100 object data set as query count is raised to 200% of object count***

## Conclusions:

• Unnecessary page accesses were reduced by 80% after clustering 1-D data


• Low query count workloads (<17) clustered better, achieving reductions of 90% with 1-D data

• High dimensional data still saw visible reductions but less substantial as dimensionality and in turn variance increased

• Sub-clustering ensures cluster quality and intracluster ordering, consistently reducing error

• Super-clustering connects cluster edges, making visually and numerically more clustered matrices

## Discussion & Future Steps:

• These findings demonstrate feasibility of using clustering to accomplish data partitioning

• K-means, a relatively simple clustering algorithm produced substantial reductions in unnecessary storage operations

• Explore the applications of advanced clustering algorithms such as Principal component analysis (PCA) that could prove to be more accurate and effective than K-means

• Current approach to physical ordering of partitions not ideal, move toward more effective method

• How to search/index/discard pages when querying

## References: 

1. Novikov, Andrei. “PyClustering: Data Mining Library.” Journal of Open Source Software, vol. 4, no. 36, Apr. 2019, p. 1230. DOI.org (Crossref), doi:10.21105/joss.01230.
2. Ramakrishnan, Raghu, and Johannes Gehrke. Database Management Systems. 3rd ed, McGraw-Hill, 2003.
3. Tan, Pang-Ning, et al. Introduction to Data Mining. 1st ed, Pearson Addison Wesley, 2006.
