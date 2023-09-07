from wordcloud import WordCloud
import matplotlib.pyplot as plt
import json

def generate_wordcloud(data):
    all_keywords = ' '.join([' '.join(entry['keywords']) for entry in data if entry['date'] != '0000-00-00'])

    wordcloud = WordCloud(width=800, height=800,
                          background_color='white',
                          min_font_size=10,
                          font_path='/System/Library/Fonts/Supplemental/Songti.ttc'  # 请替换为您系统中的实际字体路径
                          ).generate(all_keywords)

    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)

    plt.show()

with open('/Users/bernoulli_hermes/projects/python_summer/refined_pages.json', 'r') as f:
    data = json.load(f)

generate_wordcloud(data)
