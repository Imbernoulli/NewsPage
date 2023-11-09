import matplotlib
import matplotlib.pyplot as plt
import json
from collections import defaultdict
import pandas as pd
import os

from matplotlib.font_manager import FontProperties

font = FontProperties(fname='/System/Library/Fonts/Supplemental/Songti.ttc')


def analyze_keyword_trends(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    all_keywords = ['AI', '苹果', '投资', '巴菲特', '科技行业', '特斯拉', '网络文化', '马斯克', '苹果股票', '华为', '微软', '新能源汽车', '小米', '财报', '推特', '谷歌', '营收', '腾讯', '股价', '比亚迪', '芯片', '元宇宙', '三星', '亏损', '销量', '净利润', '美元', '蔚来', '宁德时代', '电动汽车', '裁员', 'Meta', 'ChatGPT', '亚马逊', '京东', 'iPhone', '供应链', '抖音', '直播', '美国', '其他']
    
    trend_count = defaultdict(lambda: defaultdict(int))
    total_count = defaultdict(int)
    
    for entry in data:
        date = entry['date'][:7]
        keywords = entry['keywords']
        
        for keyword in all_keywords:
            if keyword in keywords:
                trend_count[date][keyword] += 1
        
        total_count[date] += 1
    
    df = pd.DataFrame.from_dict(trend_count, orient='index', columns=all_keywords).fillna(0)
    df.sort_index(inplace=True)
    for keyword in all_keywords:
        df[keyword] /= total_count[date]
    plt.figure(figsize=(20, 10))
    plt.stackplot(df.index, *[df[keyword] for keyword in all_keywords], labels=all_keywords)
    plt.legend(loc='upper left', prop=font, bbox_to_anchor=(1,1)) 
    plt.title("关键词每月热度", fontproperties=font)
    plt.xlabel("年-月", fontproperties=font)
    plt.ylabel("热度", fontproperties=font)
    plt.xticks(rotation=45) 
    plt.tight_layout(rect=[0,0,0.85,1]) 
    plt.savefig("stacked_area_chart.png")


analyze_keyword_trends('/Users/bernoulli_hermes/projects/python_summer/refined_pages.json')
