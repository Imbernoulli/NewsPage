import json
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

with open("/Users/bernoulli_hermes/projects/python_summer/refined_pages.json", "r") as f:
    data = json.load(f)

seg_counter = Counter()

for item in data:
    segdict = item.get("segdict", {})
    for seg, count in segdict.items():
        seg_counter[seg] += count

wordcloud = WordCloud(width=800, height=400, background_color="white",font_path='/System/Library/Fonts/Supplemental/Songti.ttc' ).generate_from_frequencies(seg_counter)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
