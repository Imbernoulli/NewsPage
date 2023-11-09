# Experiment Report

**Class28 Bohan Lyu 2022011547**

## Web Crawling Section

### Implemented Crawlers and Methods

1. Crawling Sina News List (`read_list.py`)

Method: Use the `Selenium` package for dynamic crawling. To improve efficiency, ChromeOptions is used to set the headless browser. Over 20,000 news links were crawled from 2022-01-01 to 2023-08-30 and stored in `sina_link.txt`.

2. Crawling Sina News Content Page (`read_page.py`)

There are three different formats for the content page of Sina News. The first two are common formats, but some articles have responsible editors, while others do not. Articles with responsible editors also have authors (names) and sources (newspaper names). To obtain more accurate data, the crawlers I designed for these two situations are slightly different, so as to fully record the article information. The third form is that clicking the link will jump to the "Genesis" column, the format of this content page is quite different from the first two, and a separate crawler needs to be designed. At the same time, this content page has the author's information and the link to the author's Sina News homepage. I will jump to the Sina News to crawl the number of fans of the author.

At the same time, if the request library is used to crawl the content page, some pages cannot get comment information because the comment information on the content page is dynamically loaded. Therefore, all content pages use Selenium for crawling. Selenium is much slower than request, so I have opened many threads to crawl at the same time.

3. Crawling the number of fans of the author's Sina Weibo (`fixjson.py`)

The method of Sina Weibo to prevent crawlers is complex. It is necessary to first obtain various cookies (`weibo_cookies.json`) through the code (`get_weibo_cookies.py`), and then import all these cookies into the browser of Selenium after opening the news page, and perform dynamic crawling.

3. Search for the author by name through the Sina Weibo homepage and obtain the author's homepage (`get_weibo_fans.py`)

Considering that most news does not provide the link to the author's Sina Weibo homepage, I used the more complex functions of Selenium to simulate the functions of positioning, clicking, inputting, and deleting pages on the web page. By entering the name of the news author on the homepage to search, the author's homepage link is obtained, and then return to 3 to crawl the number of fans of the author's Sina Weibo. However, some authors' Weibo have been deleted, and some authors do not have Sina Weibo. In these cases, the number of fans of the author is recorded as 0.

### Data Processing

1. **Obtain the pure text information of the main text:** The main text directly crawled contains various html functions, not only the signs before and after each paragraph, but also the signs in the text (such as stock information jump). In order to have a good display on my own page, the main text information and picture links are accurately extracted through regular expressions.

2. **Add keywords to the article:** Most of the news crawled have few or even no keywords. At this time, I use the method of Few-Shot Learning to use gpt-3.5-turbo to add keywords to the article. The specific implementation method is to let AI return suitable keywords in a fixed format based on the content of the article through an appropriate promt (`query_format.md`), and then extract keywords from the answer through regular expressions.

3. **Add pictures to the article:** Some articles do not have a picture. For aesthetics (every article has a picture when displaying the news list), I will first automatically call ChatGPT to translate the title of the article into English, and then automatically use unsplash to generate corresponding photos for the article and download them locally.

4. **Word segmentation processing:** Use jieba to perform word segmentation processing for each article separately, and filter out word segments of length 1 that are not very meaningful. And stored in the database. A total of more than 230,000 separate word segments were obtained.

5. **Simulate article heat:** Many articles have already obtained the number of fans of the author, and my article heat is simulated with Gaussian noise. I first got the number of fans of the author of all the articles with the author's fans, and then calculated its mean and variance information.

   Let the set of all articles with the author's fans be \( A \), where the number of fans of article \( i \) is \( $f_i$ \).

   - **Mean:** $[ \mu = \frac{\sum_{i \in A} f_i}{|A|} ]$
   - **Variance:** $[ \sigma^2 = \frac{\sum_{i \in A} (f_i - \mu)^2}{|A|} ]$

   Next, for the set of articles without the author's fans \( B \), we use Gaussian noise to simulate its heat.

   - **Simulated heat (simulate articles without fans):** $[ H_{\text{no\_fans}} = \mu + \epsilon ]$
     Where, \($\epsilon$) is Gaussian noise with a mean of 0 and a variance of \( $\sigma^2$ \).

   For the set of articles with fans \( A \), we add Gaussian noise with a mean of 0.

   - **Simulated heat (simulate articles with fans):** $[ H_{\text{with\_fans}} = f_i + \epsilon ]$
     Where, \($\epsilon$) is Gaussian noise with a mean of 0 and a variance of \( $\sigma^2$ \).

| ![Article Heat Flow Chart](https://cdn.jsdelivr.net/gh/Imbernoulli/mdimages@main/%E6%96%87%E7%AB%A0%E7%83%AD%E5%BA%A6%E6%B5%81%E7%A8%8B%E5%9B%BE.png) | ![Flow Chart](https://cdn.jsdelivr.net/gh/Imbernoulli/mdimages@main/%E6%B5%81%E7%A8%8B%E5%9B%BE.png) |
| ------------------------------------------------------------ | ------------------------------------------------------------ |

## Web Page Building Section

### Models and Data

![classes_Pyreverse](https://cdn.jsdelivr.net/gh/Imbernoulli/mdimages@main/classes_Pyreverse.png)

I defined the above models in Django's models.py, and fully utilized its one-to-many (ForeignField), many-to-many (ManytomangField) to establish connections between different classes. The relationship between the author and the news is one-to-many, SegName (word segmentation name) and Segcontent (word segmentation information) are also one-to-many, and the relationship between the article and the keyword is many-to-many. The definition of these relationships provides great convenience for database maintenance, word modification, search, sorting, etc.

At the same time, in order to implement the segmented display of articles and consider convenience, I only store the content information of the article in the local extremely simplified file, so that the content page of the article can be segmented and the original position of the picture in the text can be retained.

![Screenshot 2023-09-05 23.40.31](https://cdn.jsdelivr.net/gh/Imbernoulli/mdimages@main/%E6%88%AA%E5%B1%8F2023-09-05%2023.40.31.png)

### Classification, Search and Sorting

Classification: I use the keywords marked by AI in the article for classification. I selected the top 40 keywords in frequency as 40 categories, and added the classification options of "all" and "others". Selecting categories in the multi-selection box will get the union of the articles contained in these keywords.

Search: This article implements four search methods: date search, keyword search, sentence search (exact search), and word segmentation search. Date search is to get all the news of that date; keyword search takes the intersection of all input keywords (the union has been implemented in the previous function). Sentence search is to accurately determine whether the title and content of the article contain search content; word segmentation search is to use jieba to process the input and match it with the word segmentation in the database.

Sorting: This article implements four sorts: reverse chronological order, chronological order, heat sorting, relevance (word segmentation relevance) sorting, and also uses reverse chronological order for comment display.

Result: The specific algorithm uses classification filtering first, then uses search to narrow the range, and finally sorts to improve search efficiency. Most complex searches will end within 0.3 seconds and give accurate results.

Implementation example:

Text search:

`from django.db.models import Q`

`possible_news = possible_news.filter(`

​            `Q(news_title__icontains=content) |`

​            `Q(news_content__icontains=content)`

​        `)`

Reverse chronological order:

`news_objects = possible_news.order_by('-pub_date')`

The rest of the specific code is in the `search()` function in `mynews/newspage/views.py`.

### Web Page Display

I improved the aesthetics of the web page by using some components of bootstrap. The css file of bootstrap and all the required photos are loaded to the front end through static documents. (The content of the static document is too large, there are more than 60,000 pictures in total, and it has not been submitted.)

Web page display:

![Screenshot 2023-11-09 13.24.01](https://cdn.jsdelivr.net/gh/Imbernoulli/mdimages@main/%E6%88%AA%E5%B1%8F2023-11-09%2013.24.01.png)

![Screenshot 2023-11-09 13.24.25](https://cdn.jsdelivr.net/gh/Imbernoulli/mdimages@main/%E6%88%AA%E5%B1%8F2023-11-09%2013.24.34.png)

![Screenshot 2023-11-09 13.24.47](https://cdn.jsdelivr.net/gh/Imbernoulli/mdimages@main/%E6%88%AA%E5%B1%8F2023-11-09%2013.24.47.png)