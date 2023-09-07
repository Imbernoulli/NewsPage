import json
from collections import defaultdict
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import os

from matplotlib.font_manager import FontProperties

font = FontProperties(fname='/System/Library/Fonts/Supplemental/Songti.ttc')

def analyze_keyword_trends(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    keyword_count_by_month = defaultdict(lambda: defaultdict(int))
    total_count_by_month = defaultdict(int)
    all_keywords = ['AI', '苹果', '投资', '巴菲特', '科技行业', '特斯拉', '网络文化', '马斯克', '苹果股票', '华为', '微软', '新能源汽车', '小米', '财报', '推特', '谷歌', '营收', '腾讯', '股价', '比亚迪', '芯片', '元宇宙', '三星', '亏损', '销量', '净利润', '美元', '蔚来', '宁德时代', '电动汽车', '裁员', 'Meta', 'ChatGPT', '亚马逊', '京东', 'iPhone', '供应链', '抖音', '直播', '美国', '其他']
    
    for entry in data:
        date = entry['date']
        year_month = date[:7]
        total_count_by_month[year_month] += 1
        for keyword in entry['keywords']:
            if keyword in all_keywords:
                keyword_count_by_month[year_month][keyword] += 1

    keyword_heat_by_month = defaultdict(dict)
    for year_month in keyword_count_by_month:
        total_count = total_count_by_month[year_month]
        for keyword in all_keywords:
            keyword_count = keyword_count_by_month[year_month].get(keyword, 0)
            keyword_heat_by_month[year_month][keyword] = keyword_count / total_count

    df = pd.DataFrame(keyword_heat_by_month).T.fillna(0)
    df.sort_index(inplace=True)
    for keyword in all_keywords:
        plt.figure(figsize=(14, 7))
        plt.plot(df.index, df[keyword], label=keyword)
        plt.legend(loc='upper right',prop=font, bbox_to_anchor=(1,1))
        plt.title(f"{keyword} 每月热度",fontproperties=font)
        plt.xlabel("年-月",fontproperties=font)
        plt.ylabel("热度",fontproperties=font)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig( f"resultimgs/{keyword}.png")
        plt.close()

analyze_keyword_trends('/Users/bernoulli_hermes/projects/python_summer/refined_pages.json')
