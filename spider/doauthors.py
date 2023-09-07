import json

with open("author.txt","r") as f:
    authors=f.readlines()

authors=[author.strip("\n").split(" ") for author in authors]
authorjson=[]

for i in range(len(authors)):
    if authors[i][0] in [author["name"] for author in authorjson]:
        continue
    if i>=1:
        if len(authors[i])>3:
            print(authors[i])
        elif authors[i][1]==authors[i-1][1]:
            continue
        else:
            if "万" in authors[i][1]:
                authors[i][1]=int(float(authors[i][1].strip("万"))*10000)
            elif "亿" in authors[i][1]:
                authors[i][1]=int(float(authors[i][1].strip("亿"))*100000000)
            elif ""==authors[i][1]:
                authors[i][1]=0
            else:
                authors[i][1]=int(authors[i][1])
            authorjson.append({"name":authors[i][0],
                               "fans":authors[i][1],
                               "link":authors[i][2]})
with open("authors.json","w") as f:
    f.write(json.dumps(authorjson, indent=4, ensure_ascii=False))