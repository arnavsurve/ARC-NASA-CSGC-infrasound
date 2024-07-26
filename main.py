import infrapy
from obspy import read
import infrapy.detection
import infrapy.utils
import matplotlib.pyplot as plt

# read MiniSEED data
stream = read('./datasets/Data_for_Forecasting_the_Eruption_of_an_Open_vent_Volcano_Using_Resonant_Infrasound_Tones_Johnson/VIC_miniSEED - Jeffrey B Johnson/VIC_02140000.ms')

print(stream)

# # filter data
# filtered_stream = infrapy.utils.filter_stream(stream, freqmin=0.5, freqmax=5.0)
#
# # run detection
#
# detections = infrapy.detection.run_sta_lta(filtered_stream, sta=1, lta=10)
#
# # plot detections
# for trace in filtered_stream:
#     plt.plot(trace.times(), trace.data, label=trace.id)
#
# plt.legend()
# plt.show()
