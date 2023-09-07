from matplotlib.font_manager import FontProperties
import json
import random
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from tqdm import tqdm
from sklearn.metrics import accuracy_score
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
font = FontProperties(fname='/System/Library/Fonts/Supplemental/Songti.ttc')
def get_hidden_layer_output(mlp, X):
    activation = X
    for i in range(len(mlp.coefs_) - 1):
        activation = np.dot(activation, mlp.coefs_[i]) + mlp.intercepts_[i]
        activation = np.tanh(activation)
        # activation = np.relu(activation)
    return activation

with open('/Users/bernoulli_hermes/projects/python_summer/refined_pages.json', 'r') as f:
    data = json.load(f)
all_keywords = ['AI', '苹果', '投资', '巴菲特', '科技行业', '特斯拉', '网络文化', '马斯克', '苹果股票', '华为', '微软', '新能源汽车', '小米', '财报', '推特']
num_train = int(0.7 * len(all_keywords))
training_keywords = all_keywords[:num_train]
testing_keywords = all_keywords[num_train:]
all_segnames = list(set(seg for entry in data for seg in entry['segdict']))
seg_to_index = {seg: i for i, seg in enumerate(all_segnames)}

X = []
y = []

for entry in data:
    features = np.zeros(len(seg_to_index))
    for seg, count in entry['segdict'].items():
        if seg in seg_to_index:
            features[seg_to_index[seg]] = count
    label = next((keyword for keyword in entry['keywords'] if keyword in all_keywords), None)
    if label:
        X.append(features)
        y.append(label)

X = np.array(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# mlp = MLPClassifier(hidden_layer_sizes=(240,180,120,), max_iter=50)
# mlp.fit(X_train, y_train)

# y_pred = mlp.predict(X_test)
# print("Accuracy:", accuracy_score(y_test, y_pred))

# hidden_layer_output = get_hidden_layer_output(mlp, X_test)

tsne = TSNE(n_components=3)
X_test_tsne = tsne.fit_transform(X_test)
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

colors = plt.cm.jet(np.linspace(0, 1, len(all_keywords)))

for idx, keyword in enumerate(all_keywords):
    indices = [i for i, label in enumerate(y_test) if label == keyword]
    if indices:
        ax.scatter(X_test_tsne[indices, 0], X_test_tsne[indices, 1], X_test_tsne[indices, 2], c=[colors[idx]], label=keyword)

ax.set_title('X_test', fontproperties=font)
ax.legend(prop=font)
plt.show()