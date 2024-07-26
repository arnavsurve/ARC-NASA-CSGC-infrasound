import os
from obspy import read
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

valid_extensions = ('.ms', '.mseed')

dataset_dir = './datasets/Data_for_Forecasting_the_Eruption_of_an_Open_vent_Volcano_Using_Resonant_Infrasound_Tones_Johnson/VIC_miniSEED - Jeffrey B Johnson/'
miniseed_files = [os.path.join(dataset_dir, f) for f in os.listdir(dataset_dir) if f.endswith(valid_extensions)]
print(miniseed_files, "\n")

"""
# recurively search for MiniSEED files in a directory and subdirectories

miniseed_files = []
for root, dirs, files in os.walk(dataset_dir):
    for file in files:
        if file.endswith(valid_extensions):
            miniseed_files.append(os.path.join(root, file))
"""


# function to extract features from a trace
def extract_features(trace):
    return np.array([
        trace.data.mean(),
        trace.data.std(),
        trace.data.max(),
        trace.data.min()
    ])

data = []
labels = []

# read MiniSEED data
for file in miniseed_files:
    st = read(file)
    for tr in st:
        features = extract_features(tr)
        data.append(features)
        labels.append(file.split('/')[-1].split('_')[0])

x = np.array(data)
y = np.array(labels)

# split the data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# create a random forest classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(x_train, y_train)

# evaluate the model
predictions = clf.predict(x_test)
print(classification_report(y_test, predictions))
