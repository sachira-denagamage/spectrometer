import pandas as pd
import matplotlib.pyplot as plt

spectra_1 = '/Users/sachira/Desktop/Code/spectrometer/projector-measurements/single_lens_with_screen.csv'
spectra_2 = '/Users/sachira/Desktop/Code/spectrometer/projector-measurements/single_lens_no_screen.csv'

df1 = pd.read_csv(spectra_1)
df2 = pd.read_csv(spectra_2)

df1 = df1[(df1['wavelengths'] >= 350) & (df1['wavelengths'] <= 650)]
df2 = df2[(df2['wavelengths'] >= 350) & (df2['wavelengths'] <= 650)]

ratio = df1['spectra'] / df2['spectra']

plt.plot(df1['wavelengths'], ratio)
plt.xlabel('Wavelengths (nm)')
plt.ylabel('Spectra Ratio')
plt.ylim(-1, 1)
plt.show()