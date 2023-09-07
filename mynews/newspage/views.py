from django.shortcuts import render
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.views.generic import ListView
from collections import defaultdict
from django.db.models import Q
from urllib.parse import urlencode
from django.db.models import Sum
import random
import json
from datetime import date,datetime
from .models import News,Author,Keywords,Comment,SegName,Segcontent
from django.http import HttpResponse
import jieba
import time
from collections import defaultdict

def index(request):
    random_ids = random.sample(range(1,20001), 20)
    random_news = News.objects.filter(news_id__in=random_ids)
    context={'list':random_news}
    return render(request,'newspage/index.html',context)

def allnews(request):
    start_time = time.time()
    query_dict = {
        'searchType': "关键词搜索",
        'query': "全部",
        'sort': "time1",
        'keywords': ["全部"]
    }
    page = max(1, int(request.GET.get('page', 1)))
    possible_news=News.objects.all()
    
    query_string = urlencode(query_dict, doseq=True)
    
    end_time = time.time()
    search_time = end_time - start_time
    
    paginator = Paginator(possible_news, 20)
    sorted_news = paginator.page(page)
    
    return render(request, "newspage/list.html", {
        "list": sorted_news,
        "search_time": search_time,
        "query_string": query_string
    })

def page(request,newsid):
    news = News.objects.get(news_id=newsid)
    comments = news.comment_set.all().order_by('-comment_time')
    with open("/Users/bernoulli_hermes/projects/python_summer/concise_pages.json","r") as f:
        pages=json.loads(f.read())
    contents=pages[str(newsid)]
    context = {
        'news': news,
        'comments': comments,
        'news_content':contents
    }
    return render(request, 'newspage/contentpage.html', context)

def dirhome(request):
    return render(request,'newspage/homepage.html')

def searchpage(request):
    return render(request,'newspage/search.html',{"list":['全部', 'AI', '苹果', '投资', '巴菲特', '科技行业', '特斯拉', '网络文化', '马斯克', '苹果股票', '华为', '微软', '新能源汽车', '小米', '财报', '推特', '谷歌', '营收', '腾讯', '股价', '比亚迪', '芯片', '元宇宙', '三星', '亏损', '销量', '净利润', '美元', '蔚来', '宁德时代', '电动汽车', '裁员', 'Meta', 'ChatGPT', '亚马逊', '京东', 'iPhone', '供应链', '抖音', '直播', '美国', '其他']})

def create_comment(request, news_id):
    if request.method == 'POST':
        comment_content = request.POST.get('comment_content')
        comment_user = request.POST.get('comment_user')

        comment = Comment(comment_content=comment_content, comment_user=comment_user, its_article=News.objects.get(news_id=news_id))
        comment.save()

    return redirect(f'/search/{news_id}')

def delete_comment(request, comment_id, news_id):
    try:
        comment = Comment.objects.get(pk=comment_id)
        comment.delete()
    except:
        pass

    return redirect(f'/search/{news_id}')

def search(request):
    start_time = time.time()
    search_type = request.GET.get('searchType', '文本搜索')
    content = request.GET.get('query', '全部')
    sort = request.GET.get('sort', 'time1')
    keywords = request.GET.getlist('keywords',["全部"])
    page = max(1, int(request.GET.get('page', 1)))
    query_dict = {
        'searchType': search_type,
        'query': content,
        'sort': sort,
        'keywords': keywords
    }

    if '全部' in keywords:
        possible_news = News.objects.all()
    else:
        possible_news = News.objects.filter(its_keywords__word_name__in=keywords)

    if search_type == "关键词搜索":
        wordlist = content.split(" ")
        # if '全部' not in wordlist:
        #     possible_news = possible_news.filter(its_keywords__word_name__in=wordlist)
        
        # if '全部' not in wordlist:
        #     queries = [Q(its_keywords__word_name=word) for word in wordlist]
        #     query = queries.pop()
            
        #     for item in queries:
        #         query |= item
            
        #     possible_news = News.objects.filter(query).distinct()
        if '全部' not in wordlist:
            possible_news = News.objects.all()
            for word in wordlist:
                possible_news = possible_news.filter(its_keywords__word_name=word)

    elif search_type == "日期搜索":
        try:
            pub_date = datetime.strptime(content, '%Y %m %d').date()
            possible_news = possible_news.filter(pub_date=pub_date)
        except ValueError:
            return render(request, "newspage/error.html", {"result": "日期格式不正确"})
    
    elif search_type == "文本搜索":
        possible_news = possible_news.filter(
            Q(news_title__icontains=content) |
            Q(news_content__icontains=content)
        )


    else:
        wordlist = list(jieba.cut_for_search(content))
        filtered_wordlist = [word for word in wordlist if len(word) > 1]
        seg_ids = SegName.objects.filter(seg_name__in=filtered_wordlist).values_list('id', flat=True)
        all_seg_contents = Segcontent.objects.filter(its_seg_id__in=seg_ids).values_list('its_article', flat=True)
        possible_news = possible_news.filter(news_id__in=all_seg_contents)

    if sort == "time1":
        news_objects = possible_news.order_by('-pub_date')
    elif sort == "time2":
        news_objects = possible_news.order_by('pub_date')
    elif sort == "popularity":
        news_objects = possible_news.order_by('-news_popularity')
    else:
        possible_news=possible_news.values_list('news_id', flat=True)
        segcontent_scores = Segcontent.objects.filter(its_article__in=possible_news).values('its_article').annotate(total_score=Sum('score'))
        segcontent_score_dict = {item['its_article']: item['total_score'] for item in segcontent_scores}
        news_objects = News.objects.filter(news_id__in=possible_news)
        news_objects = sorted(news_objects, key=lambda x: segcontent_score_dict.get(x.news_id, 0), reverse=True)

    print(news_objects)
    paginator = Paginator(news_objects, 20)
    sorted_news = paginator.page(page)
    
    end_time = time.time()
    search_time = end_time - start_time
    
    query_string = urlencode(query_dict, doseq=True)

    return render(request, "newspage/list.html", {
        "list": sorted_news, 
        "search_time": search_time, 
        "query_string": query_string
    })

def cat(request):
    list1=['全部', 'AI', '苹果', '投资', '巴菲特', '科技行业', '特斯拉', '网络文化', '马斯克', '苹果股票', '华为', '微软', '新能源汽车', '小米', '财报', '推特', '谷歌', '营收', '腾讯', '股价', '比亚迪', '芯片', '元宇宙', '三星', '亏损', '销量', '净利润', '美元', '蔚来', '宁德时代', '电动汽车', '裁员', 'Meta', 'ChatGPT', '亚马逊', '京东', 'iPhone', '供应链', '抖音', '直播', '美国', '其他']
    list2=[20000,2856, 2529, 2440, 2386, 1596, 1512, 1247, 846, 814, 698, 613, 530, 502, 482, 479, 477, 464, 462, 445, 439, 417, 405, 404, 378, 375, 353, 352, 346, 330, 328, 325, 300, 298, 295, 293, 293, 283, 282, 280, 271,9055]
    combined = zip(list1, list2)
    return render(request,'newspage/newscat.html',{"lists":combined})

def kw(request,keyword):
    start_time = time.time()
    query_dict = {
        'searchType': "关键词搜索",
        'query': keyword,
        'sort': "popularity",
        'keywords': [keyword]
    }
    page = max(1, int(request.GET.get('page', 1)))
    if '全部' == keyword:
        possible_news = News.objects.all()
    else:
        possible_news = News.objects.filter(its_keywords__word_name__in=[keyword])
        
    query_string = urlencode(query_dict, doseq=True)
    
    end_time = time.time()
    search_time = end_time - start_time
    
    paginator = Paginator(possible_news, 20)
    sorted_news = paginator.page(page)
    
    return render(request, "newspage/list.html", {
        "list": sorted_news, 
        "search_time": search_time, 
        "query_string": query_string
    })