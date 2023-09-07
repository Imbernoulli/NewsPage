import json
import datetime
import pandas as panda
from datetime import date, timedelta
from tqdm import tqdm
import math

with open("/Users/bernoulli_hermes/projects/python_summer/refined_pages.json","r") as f:
    refpages=json.loads(f.read())
    
all_seg={}
all_keywords={}
all_date_features={}

for page in tqdm(refpages):
    for seg,num in page["segdict"].items():
        mine={"index":page["index"],"num":num}
        if seg in all_seg:
            all_seg[seg].append(mine)
        else:
            all_seg[seg]=[mine]

new_seg={}
for seg,dit in tqdm(all_seg.copy().items()):
    num=0
    new_dit=sorted(dit,key=lambda x:x["num"],reverse=True)
    new_seg[seg]=new_dit
    length=len(new_seg[seg])
    for i in new_seg[seg]:
        num+=1
        i["tfidf"]=i["num"]*(math.log10(20000/length))
        i["ranking"]=num
        del i["num"]

with open("seg.json","w") as f:
    f.write(json.dumps(new_seg, indent=4, ensure_ascii=False))

# for page in tqdm(refpages):
#     # mine={"index":page["index"]}
#     mine=page["index"]
#     for keyword in page["keywords"]:
#         if keyword in all_keywords:
#             all_keywords[keyword].append(mine)
#         else:
#             all_keywords[keyword]=[mine]
# all_keywords=sorted(all_keywords.items(),key=lambda x:len(x[1]),reverse=True)
# all_keywords = {k: v for k, v in all_keywords}
# with open("keywords.json","w") as f:
#     f.write(json.dumps(all_keywords, indent=4, ensure_ascii=False))

# date1 = datetime.datetime(2022, 1, 1)
# date2 = datetime.datetime(2023, 8, 30)
# current_date=date1
# dates=[]
# while current_date<=date2:
#     dates.append(current_date.strftime("%Y-%m-%d"))
#     current_date+=timedelta(days=1)
    
# for date in tqdm(dates):    
#     date_feature={}
#     pages=[]
#     for page in refpages:
#         if date==page["date"]:
#             pages.append(page)
#     date_feature["all_articles"]=pages
#     date_feature["num_keywords"]=sum(len(page["comments"]) for page in pages)
#     date_keywords={}
#     for page in pages:
#         mine={"index":page["index"]}
#         for keyword in page["keywords"]:
#             if keyword in all_keywords:
#                 date_keywords[keyword].append(mine)
#             else:
#                 date_keywords[keyword]=[mine]
#     all_date_features[date]=date_feature