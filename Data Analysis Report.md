# Experiment Report

**Class28 Bohan Lyu 2022011547**

### 1. Changes in public focus points obtained by drawing a keyword heat map from January 2022 to August 2023

The definition of keyword heat is the number of articles containing the keyword this month / the total number of articles this month. Because the absolute number of articles each month may be different, the absolute number of news corresponding to the news category may not be meaningful, but this ratio is meaningful.

I have drawn line charts for each of the 40 keywords I selected, and also drawn cumulative charts for these keywords.

Cumulative chart:

![stacked_area_chart](https://cdn.jsdelivr.net/gh/Imbernoulli/mdimages@main/stacked_area_chart.png)

Example of line chart:

![截屏2023-11-09 13.49.59](https://cdn.jsdelivr.net/gh/Imbernoulli/mdimages@main/%E6%88%AA%E5%B1%8F2023-11-09%2013.49.59.png)

The first row from left to right are: keyword BYD, keyword NIO

The second row from left to right are: keyword AI, keyword new energy vehicles

**Conclusion 1:** The attention to AI has been gradually increasing over the past two years, while the attention to new energy vehicles has shown a downward trend by 2023.

**Conclusion 2:** The heat trends of closely related keywords are similar. For example, the above BYD and NIO are both keywords for the concept of new energy vehicles, and their trends are similar to the trend of the keyword new energy vehicles. The same trend is reflected in the Tesla and CATL keywords that were not listed above but also got pictures (CATL is a manufacturer of new energy vehicle batteries), which also reflects that the trend changes in similar industries are similar.


### 2. Doc2Vec: Word segmentation + TSNE

  Doc2Vec schematic diagram:
  ![Screenshot 2023-09-05 23.01.37](https://cdn.jsdelivr.net/gh/Imbernoulli/mdimages@main/%E6%88%AA%E5%B1%8F2023-09-05%2023.01.37.png)

![Screenshot 2023-11-09 13.27.08](https://cdn.jsdelivr.net/gh/Imbernoulli/mdimages@main/%E6%88%AA%E5%B1%8F2023-11-09%2013.27.08.png)

![Screenshot 2023-11-09 13.27.38](https://cdn.jsdelivr.net/gh/Imbernoulli/mdimages@main/%E6%88%AA%E5%B1%8F2023-11-09%2013.27.38.png)

**Implementation method:** I processed each article into a vector of about 200,000 dimensions according to the word segmentation results (each word corresponds to a dimension), and the value of this dimension for each article is the number of this word in this article. Then use TSNE to draw these data into two-dimensional or three-dimensional data and visualize it, and finally use keywords to color each article corresponding point. From the results, the points corresponding to the articles corresponding to different keywords have shown obvious aggregation.

The red points in some of the pictures are the "Xiaomi" keyword, and the blue points are the "ChatGPT" keyword. These two keywords basically have no overlapping articles, so there is a clear division.

**Conclusion 3:** The word segmentation results of the article contain the information of the article. Processing the word segmentation vector with TSNE can classify the articles well.

### 3. Doc2Vec Plus: Word segmentation + MLP + TSNE
   
    ![Screenshot 2023-09-05 23.02.13](https://cdn.jsdelivr.net/gh/Imbernoulli/mdimages@main/%E6%88%AA%E5%B1%8F2023-09-05%2023.02.13.png)

Even if the above results are already good, the 200,000-dimensional word segmentation vector contains a lot of useless information. I found a method, adding a deep perception neural network (MLP) between the word segmentation vector and TSNE, training it to perform classification tasks through training, and then taking the vector from each analysis vector to the last hidden layer of MLP as the input vector of TSNE.

The following is the result of a classification task for two keywords (TSNE processed to two dimensions): (Blue and yellow are CATL and Xiaomi respectively)

<img src="https://cdn.jsdelivr.net/gh/Imbernoulli/mdimages@main/%E6%88%AA%E5%B1%8F2023-11-09%2013.28.08.png" alt="Screenshot 2023-11-09 13.28.08" style="zoom:50%;" />

![Screenshot 2023-11-09 13.28.38](https://cdn.jsdelivr.net/gh/Imbernoulli/mdimages@main/%E6%88%AA%E5%B1%8F2023-11-09%2013.28.38.png)

The above are the results with more keyword annotations. The two on the left are drawn directly using the test set, and the two on the right are drawn using the results of the last hidden layer of the test set data. It can be seen that although different colors (keywords) in the two pictures on the left also have aggregation, it is not very obvious, while the two pictures on the right are very obvious.

**Conclusion 4:** Adjusting the weight of each dimension of the word segmentation through MLP can allow TSNE to better visualize and classify, and can better reflect the characteristics of the article.