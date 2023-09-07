from typing import Any
from django.db import models
from datetime import date, datetime

# Create your models here.
# class NewsManager(models.Manager):
#     def create(self,title,date,popularity,author):
#         news=self.model()
#         news.news_title=title
#         news.pub_date=date
#         news.news_popularity=popularity
#         news.author=author
#         news.isDelete = False
#         return news

class News(models.Model):
    news_id=models.IntegerField() 
    news_link=models.CharField(max_length=100)
    news_title=models.CharField(max_length=40)
    news_content=models.TextField()
    news_summary=models.CharField(max_length=60)
    pub_date = models.DateField()
    news_popularity=models.IntegerField()
    author=models.ForeignKey("Author",on_delete=models.CASCADE)
    # newsmanager=NewsManager()
    its_keywords=models.ManyToManyField("Keywords")
    objects=models.Manager()
    def __str__(self):
        return self.news_title

# class AuthorManager(models.Manager):
#     def create(self,name,fans):
#         author=self.model()
#         author.author_name=name
#         author.author_fans=fans
#         return author

class Author(models.Model):
    author_name=models.CharField(max_length=10)
    author_fans=models.IntegerField()
    author_link=models.CharField(max_length=36)
    # authormanager=AuthorManager()
    objects=models.Manager()
    def __str__(self):
        return self.author_name

class Keywords(models.Model):
    objects=models.Manager()
    word_name=models.CharField(max_length=8)
    its_article=models.ManyToManyField(to="News")

class CommentManager(models.Manager):
    def create_comment(self, comment_user, comment_content, its_article):
        comment = self.create( comment_user=comment_user, comment_content=comment_content, its_article=its_article)
        return comment
    
    def delete_comment(self, id):
        comment = self.get(id=id)
        comment.delete()

class Comment(models.Model):
    comment_user=models.CharField(max_length=30)
    comment_content=models.TextField()
    its_article=models.ForeignKey("News",on_delete=models.CASCADE)
    comment_time = models.DateTimeField(default=datetime.now, blank=True)
    # objects=models.Manager()
    objects = CommentManager()
    def __str__(self):
        return self.comment_user+":"+self.comment_content

class SegName(models.Model):
    seg_name=models.CharField(max_length=5)
    objects=models.Manager()
    def __str__(self):
        return self.seg

class Segcontent(models.Model):
    its_article=models.IntegerField()
    its_seg=models.ForeignKey("SegName",on_delete=models.CASCADE)
    score=models.FloatField()
    objects=models.Manager()
    def __str__(self):
        return self.its_article+self.its_seg