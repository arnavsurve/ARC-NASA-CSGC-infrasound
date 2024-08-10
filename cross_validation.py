import os
from obspy import read
import numpy as np
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.model_selection import train_test_split
from sklearn.metrics import silhouette_score

valid_extensions = ('.ms', '.mseed')

dataset_dir = './datasets/Data_for_Forecasting_the_Eruption_of_an_Open_vent_Volcano_Using_Resonant_Infrasound_Tones_Johnson/VIC_miniSEED - Jeffrey B Johnson/'
miniseed_files = [os.path.join(dataset_dir, f) for f in os.listdir(dataset_dir) if f.endswith(valid_extensions)]
print(miniseed_files, "\n")

# Function to extract features from a trace
def extract_features(trace):
    return np.array([
        trace.data.mean(),
        trace.data.std(),
        trace.data.max(),
        trace.data.min()
    ])

data = []

# Read MiniSEED data
for file in miniseed_files:
    st = read(file)
    for tr in st:
        features = extract_features(tr)
        data.append(features)

x = np.array(data)

# Split data into training and test sets
x_train, x_test = train_test_split(x, test_size=0.2, random_state=42)

# Define parameter grids for hyperparameter tuning
param_grids = {
    "KMeans": {"n_clusters": [2, 3, 4, 5]},
    "DBSCAN": {"eps": [0.1, 0.3, 0.5, 0.7], "min_samples": [5, 10, 15]},
    "AgglomerativeClustering": {"n_clusters": [2, 3, 4, 5]}
}

# Evaluate each model with different hyperparameters
for name, params in param_grids.items():
    print(f'Evaluating {name} with hyperparameter tuning:')
    best_silhouette = -1
    best_params = None

    if name == "KMeans":
        for n_clusters in params["n_clusters"]:
            model = KMeans(n_clusters=n_clusters, random_state=42)
            model.fit(x_train)
            labels = model.labels_
            n_clusters_found = len(set(labels))

            if n_clusters_found > 1:
                silhouette_avg = silhouette_score(x_train, labels)
                print(f'KMeans with n_clusters={n_clusters} - Silhouette Score: {silhouette_avg}')

                if silhouette_avg > best_silhouette:
                    best_silhouette = silhouette_avg
                    best_params = {'n_clusters': n_clusters}

    elif name == "DBSCAN":
        for eps in params["eps"]:
            for min_samples in params["min_samples"]:
                model = DBSCAN(eps=eps, min_samples=min_samples)
                model.fit(x_train)
                labels = model.labels_
                n_clusters_found = len(set(labels)) - (1 if -1 in labels else 0)

                if n_clusters_found > 1:
                    silhouette_avg = silhouette_score(x_train, labels)
                    print(f'DBSCAN with eps={eps}, min_samples={min_samples} - Silhouette Score: {silhouette_avg}')

                    if silhouette_avg > best_silhouette:
                        best_silhouette = silhouette_avg
                        best_params = {'eps': eps, 'min_samples': min_samples}

    elif name == "AgglomerativeClustering":
        for n_clusters in params["n_clusters"]:
            model = AgglomerativeClustering(n_clusters=n_clusters)
            model.fit(x_train)
            labels = model.labels_
            n_clusters_found = len(set(labels))

            if n_clusters_found > 1:
                silhouette_avg = silhouette_score(x_train, labels)
                print(f'Agglomerative with n_clusters={n_clusters} - Silhouette Score: {silhouette_avg}')

                if silhouette_avg > best_silhouette:
                    best_silhouette = silhouette_avg
                    best_params = {'n_clusters': n_clusters}

    print(f'Best parameters for {name}: {best_params} with Silhouette Score: {best_silhouette}\n')

    # Test with the best parameters found
    if best_params:
        if name == "KMeans":
            model = KMeans(**best_params, random_state=42)
        elif name == "DBSCAN":
            model = DBSCAN(**best_params)
        elif name == "AgglomerativeClustering":
            model = AgglomerativeClustering(**best_params)

        model.fit(x_test)
        test_labels = model.labels_
        n_test_clusters = len(set(test_labels)) - (1 if -1 in test_labels else 0)

        if n_test_clusters > 1:
            test_silhouette_avg = silhouette_score(x_test, test_labels)
            print(f'{name} - Test Silhouette Score with best params: {test_silhouette_avg}\n')
        else:
            print(f'{name} - Only one cluster found in test data with best params.\n')

        # Output cluster assignments for test set
        for i, label in enumerate(test_labels):
            print(f'Test Sample {i}: Cluster {label}')