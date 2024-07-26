import os
from obspy import read

valid_extensions = ('.ms', '.mseed')

dataset_dir = './datasets/Data_for_Forecasting_the_Eruption_of_an_Open_vent_Volcano_Using_Resonant_Infrasound_Tones_Johnson/VIC_miniSEED - Jeffrey B Johnson/'
miniseed_files = [os.path.join(dataset_dir, f) for f in os.listdir(dataset_dir) if f.endswith(valid_extensions)]
print(miniseed_files, "\n")

for file in miniseed_files:
    st = read(file)
    print(st)
    for tr in st:
        print(tr.stats)
