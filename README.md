# Python Programming Experiment: Web Crawler and Information System

<u>This is my first assignment for the course "Program Design Training (30240522)" during the summer term of my freshman to sophomore year in the Department of Computer Science at Tsinghua University.</u>

## Experiment Objective

This project aims to create a Python-based web crawler to fetch and analyze data from various news websites. It also includes the development of a Django-based website to display the fetched data and an information retrieval system to efficiently access the data. Furthermore, the project involves data visualization and analysis to derive meaningful conclusions from the fetched data.

## Experiment Overview

The project is divided into three major parts:

1. **Web Crawler:** The web crawler is designed to fetch data from the technology sections of various news websites. The fetched data includes the title, author details (ID, profile picture, number of followers), basic information (creation time, number of reads, likes, and favorites), full text along with images and code, URL, and other relevant information. The crawler is built to handle at least 5000 news articles.

2. **Website Development:** The fetched data is displayed on a Django-based website. The website includes pages for displaying the list of news articles, individual news articles, categories, and search results. The website also includes features for searching the news articles and sorting them based on time and popularity.

3. **Data Analysis:** The fetched data is analyzed to derive meaningful conclusions. The analysis involves the use of data visualization techniques and is documented in a separate report.

## Web Crawler

The web crawler is implemented in two parts:

1. **Fetching the News List:** The script `read_list.py` uses the Selenium package to dynamically fetch the list of news articles from the Sina News website. The fetched list includes over 20,000 news articles published between January 2022 and August 2023. The list of news articles is stored in `sina_link.txt`.

2. **Fetching the News Content:** The script `read_page.py` fetches the content of each news article. The content includes the title, author details, basic information, full text, images, and URL. The script also fetches the number of followers of the author from their Sina Weibo profile.

## Data Processing

The fetched data is processed in several ways:

1. **Extracting the Text:** The full text of the news articles is extracted from the fetched HTML content using regular expressions. The extracted text is stored separately for easy access.

2. **Adding Keywords:** Keywords are added to the news articles using the GPT-3.5-turbo model. The model is trained to generate keywords based on the content of the news articles.

3. **Adding Images:** Images are added to the news articles that do not have any. The images are fetched from Unsplash based on the translated title of the news articles.

4. **Word Segmentation:** The content of the news articles is segmented into words using the Jieba library. The segmented words are stored separately for easy access.

5. **Simulating Article Popularity:** The popularity of the news articles is simulated based on the number of followers of the author. The simulation involves the addition of Gaussian noise to the follower count.

## Website Development

The website is developed using Django and includes several features:

1. **Displaying the News Articles:** The news articles are displayed on separate pages. Each page includes the title, author details, basic information, full text, images, and URL of the news article.

2. **Searching the News Articles:** The website includes a search feature that allows users to search the news articles based on the title, content, date, and keywords. The search results can be sorted based on time and popularity.

3. **Categorizing the News Articles:** The news articles are categorized based on the keywords. The website includes a separate page for each category, displaying the list of news articles in that category.

4. **Commenting on the News Articles:** The website includes a comment feature that allows users to comment on the news articles. The comments are displayed at the bottom of each news article page.

## Data Analysis

The data analysis is documented in a separate report. The report includes the analysis code and the derived conclusions. The conclusions are based on the fetched data and are supported by visualizations.

## Repository Structure

- `crawler/read_list.py`: Script for fetching the list of news articles.
- `crawler/read_page.py`: Script for fetching the content of the news articles.
- `crawler/get_weibo_cookies.py`: Script for fetching the cookies for Sina Weibo.
- `crawler/get_weibo_fans.py`: Script for fetching the number of followers of the authors.
- `crawler/fixjson.py`: Script for processing the fetched data.
- `crawler/query_format.md`: File containing the prompts for the GPT-3.5-turbo model.
- `crawler/sina_link.txt`: File containing the list of news articles.
- `crawler/weibo_cookies.json`: File containing the cookies for Sina Weibo.
- `mynews/newspage/views.py`: File containing the code for the website features.
- `mynews/newspage/models.py`: File containing the data models for the website.
- `mynews/newspage/templates/newspage`: Directory containing the HTML templates for the website.
- `mynews/newspage/static/newspage`: Directory containing the static files for the website.
- `mynews/db.sqlite3`(deleted): SQLite database for the website.
- `mynews/manage.py`: Script for managing the Django project.
