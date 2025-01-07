import os
import numpy as np
import tensorflow as tf
from obspy import read
from sklearn.model_selection import train_test_split
from sklearn.metrics import silhouette_score
from sklearn.cluster import KMeans

# Function to extract features from a trace
def extract_features(trace):
    return np.array([
        trace.data.mean(),
        trace.data.std(),
        trace.data.max(),
        trace.data.min()
    ])

def load_data(dataset_dir, valid_extensions=('.ms', '.mseed')):
    miniseed_files = [os.path.join(dataset_dir, f) for f in os.listdir(dataset_dir) if f.endswith(valid_extensions)]
    data = []

    for file in miniseed_files:
        st = read(file)
        for tr in st:
            features = extract_features(tr)
            data.append(features)

    return np.array(data)

def create_autoencoder(input_dim):
    input_layer = tf.keras.layers.Input(shape=(input_dim,))
    encoded = tf.keras.layers.Dense(64, activation='relu')(input_layer)
    encoded = tf.keras.layers.Dense(32, activation='relu')(encoded)
    encoded = tf.keras.layers.Dense(16, activation='relu')(encoded)

    decoded = tf.keras.layers.Dense(32, activation='relu')(encoded)
    decoded = tf.keras.layers.Dense(64, activation='relu')(decoded)
    decoded = tf.keras.layers.Dense(input_dim, activation='linear')(decoded)

    autoencoder = tf.keras.Model(inputs=input_layer, outputs=decoded)
    encoder = tf.keras.Model(inputs=input_layer, outputs=encoded)

    autoencoder.compile(optimizer='adam', loss='mse')
    return autoencoder, encoder

def train_autoencoder(x_train, x_test, input_dim, epochs=50, batch_size=16):
    autoencoder, encoder = create_autoencoder(input_dim)
    autoencoder.fit(x_train, x_train, epochs=epochs, batch_size=batch_size, shuffle=True, validation_data=(x_test, x_test))
    return encoder

def cluster_latent_space(encoder, x_data):
    latent_space = encoder.predict(x_data)
    kmeans = KMeans(n_clusters=2, random_state=42)
    kmeans.fit(latent_space)
    labels = kmeans.labels_
    silhouette_avg = silhouette_score(latent_space, labels)
    print(f'Silhouette Score on Latent Space: {silhouette_avg}')
    return labels

# Load data
dataset_dir = './datasets/Data_for_Forecasting_the_Eruption_of_an_Open_vent_Volcano_Using_Resonant_Infrasound_Tones_Johnson/VIC_miniSEED - Jeffrey B Johnson/'
data = load_data(dataset_dir)

# Split data into training and test sets
x_train, x_test = train_test_split(data, test_size=0.2, random_state=42)

# Train the autoencoder
input_dim = x_train.shape[1]
encoder = train_autoencoder(x_train, x_test, input_dim)

# Cluster the latent space
labels = cluster_latent_space(encoder, data)

# Output cluster assignments
for i, label in enumerate(labels):
    print(f'Sample {i}: Cluster {label}')