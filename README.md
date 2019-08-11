# Query-Driven Data-Agnostic Data Partitioning

***Background:***

• Physical layout of data is essential in ensuring range query efficiency in disk storage

• Data that answer the same query can be collocated to minimize unnecessary accesses

• With one-dimensional (1-D) integer data, reading & sorting data accomplishes this

• Data is often not integer-based and can be multi-dimensional.

• When query access patterns are unpredictable and reading physical data is either not possible or too costly, finding strong data layouts becomes an interesting problem

• Data Mining algorithms, specifically clustering, allow us to develop a possible solution

![image](https://user-images.githubusercontent.com/30887959/62838161-696fde00-bc2d-11e9-97e2-32bd8cfcf1fe.png)

***Comparison of contiguous and non-contiguous access***
