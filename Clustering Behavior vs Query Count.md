Using the same dataset from a 20x20 characteristic matrix, we clustered iterations of the dataset, incrementally adding queries to discover the patterns of the algorithm. What was found that especially in the cases of completely randomized data, as the query count begins to climb, the reliability and effectiveness of the clustering diminishes very quickly. This could be attributed to the fact that since the data is completely random, the queries are simply too different and thus the columns are way too varied and unclustered fundamentally to be able to achieve good clustering. Thus, maybe trying the clustering on patternized data sets in which more practical queries are used may achieve better results. The diagrams below show basic information about the clustering as query count goes up. I plan to add error statistics, percentages, and more info to these visualizations as well to give a better view of the results.

| ***Queries*** | ***Clustered Error As Percentage of Original Error Averaged Over 20 Runs***|
|---------------|----------------|
|      3        | 79.86% |
|      4        | 83.80% |
|      5        | 75.73%  |
|      6        | 69.60% |
|      7        | 75.14% |
|      8        | 76.50% |
|      9        | 75.28% | 
|      10       | 76.42%  |
|      11       | 82.28% |
|      12       | 83.32% |
|      13       | 84.00% |
|      14       | 83.46% |
|      15       | 88.35%  |
|      16       | 88.90% |
|      17       | 87.99% |
|      18       | 89.31% |
|      19       | 92.26%  |


![3](https://user-images.githubusercontent.com/30887959/61324775-15a5dc80-a7c8-11e9-8ac7-5e1b296ef5a2.png)
![4](https://user-images.githubusercontent.com/30887959/61324776-15a5dc80-a7c8-11e9-855e-7b2db5a76ebf.png)
![5](https://user-images.githubusercontent.com/30887959/61324777-15a5dc80-a7c8-11e9-83be-3a1524579867.png)
![6](https://user-images.githubusercontent.com/30887959/61324778-15a5dc80-a7c8-11e9-8737-a7c9f0f819c6.png)
![7](https://user-images.githubusercontent.com/30887959/61324779-15a5dc80-a7c8-11e9-951a-5426ce044020.png)
![8](https://user-images.githubusercontent.com/30887959/61324780-15a5dc80-a7c8-11e9-89c8-3005e8a36c01.png)
![9](https://user-images.githubusercontent.com/30887959/61324781-163e7300-a7c8-11e9-9deb-9273b90ab210.png)
![10](https://user-images.githubusercontent.com/30887959/61324782-163e7300-a7c8-11e9-9944-3cc3fc5b6899.png)
![11](https://user-images.githubusercontent.com/30887959/61324783-163e7300-a7c8-11e9-8f6e-38f32d553968.png)
![12](https://user-images.githubusercontent.com/30887959/61324784-163e7300-a7c8-11e9-8f18-f29bed9c95fe.png)
![13](https://user-images.githubusercontent.com/30887959/61324785-163e7300-a7c8-11e9-86eb-124f9bbc330c.png)
![14](https://user-images.githubusercontent.com/30887959/61324787-163e7300-a7c8-11e9-950e-aceead53c32a.png)
![15](https://user-images.githubusercontent.com/30887959/61324789-16d70980-a7c8-11e9-8bda-365cd26324c6.png)
![16](https://user-images.githubusercontent.com/30887959/61324791-16d70980-a7c8-11e9-8d73-557c4363d7ff.png)
![17](https://user-images.githubusercontent.com/30887959/61324792-16d70980-a7c8-11e9-85b2-97a406fae366.png)
![18](https://user-images.githubusercontent.com/30887959/61324793-16d70980-a7c8-11e9-9cda-504698ec0739.png)
![19](https://user-images.githubusercontent.com/30887959/61324794-16d70980-a7c8-11e9-8cde-c50933a8050a.png)
