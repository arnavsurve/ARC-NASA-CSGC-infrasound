import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from keras_tuner import Hyperband
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

# Define a function to build the neural network model
def build_autoencoder(hp):
    input_dim = x_train.shape[1]
    input_layer = layers.Input(shape=(input_dim,))
    
    # Varying the number of hidden layers
    x = input_layer
    for i in range(hp.Int('num_layers', 1, 3)):  # Choose between 1 to 3 layers
        units = hp.Int(f'units_{i}', min_value=16, max_value=128, step=16)
        x = layers.Dense(units, activation='relu')(x)
    
    encoded = layers.Dense(16, activation='relu')(x)  # Latent space
    
    # Decoder layers (mirroring encoder)
    for i in range(hp.Int('num_layers', 1, 3)):  # Choose between 1 to 3 layers
        units = hp.Int(f'units_decoder_{i}', min_value=16, max_value=128, step=16)
        x = layers.Dense(units, activation='relu')(encoded)
    
    decoded = layers.Dense(input_dim, activation='linear')(x)
    
    autoencoder = keras.Model(inputs=input_layer, outputs=decoded)
    autoencoder.compile(optimizer='adam', loss='mse')
    
    return autoencoder

def train_autoencoder(x_train, x_test, epochs=50, batch_size=16):
    tuner = Hyperband(
        build_autoencoder,
        objective='val_loss',
        max_epochs=epochs,
        factor=3,
        directory='autoencoder_tuning',
        project_name='autoencoder'
    )
    
    tuner.search(x_train, x_train, epochs=epochs, batch_size=batch_size, validation_data=(x_test, x_test))
    best_model = tuner.get_best_models(num_models=1)[0]
    return best_model

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

# Train the autoencoder with hyperparameter tuning
best_autoencoder = train_autoencoder(x_train, x_test)

# Extract encoder from best autoencoder
encoder = keras.Model(inputs=best_autoencoder.input, outputs=best_autoencoder.layers[-3].output)

# Cluster the latent space
labels = cluster_latent_space(encoder, data)

# Output cluster assignments
for i, label in enumerate(labels):
    print(f'Sample {i}: Cluster {label}')