import os
from obspy import read
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

valid_extensions = ('.ms', '.mseed')

dataset_dir = './datasets/Data_for_Forecasting_the_Eruption_of_an_Open_vent_Volcano_Using_Resonant_Infrasound_Tones_Johnson/VIC_miniSEED - Jeffrey B Johnson/'
miniseed_files = [os.path.join(dataset_dir, f) for f in os.listdir(dataset_dir) if f.endswith(valid_extensions)]
print(miniseed_files, "\n")

# function to extract features from a trace
def extract_features(trace):
    return np.array([
        trace.data.mean(),
        trace.data.std(),
        trace.data.max(),
        trace.data.min()
    ])

data = []

# read MiniSEED data
for file in miniseed_files:
    st = read(file)
    for tr in st:
        features = extract_features(tr)
        data.append(features)

x = np.array(data)

# Use K-Means clustering to classify the data
n_clusters = 2  # Assuming we want to classify the data into two clusters: eruption and non-eruption
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
kmeans.fit(x)

# Get cluster labels
labels = kmeans.labels_

# Evaluate the clustering
silhouette_avg = silhouette_score(x, labels)
print(f'Silhouette Score: {silhouette_avg}')

# Output cluster assignments
for i, label in enumerate(labels):
    print(f'Sample {i}: Cluster {label}')
