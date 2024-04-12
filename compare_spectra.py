import pandas as pd
import matplotlib.pyplot as plt

spectra_1 = '/Users/sachira/Desktop/Code/spectrometer/projector-measurements/no_screen.csv'
spectra_2 = '/Users/sachira/Desktop/Code/spectrometer/projector-measurements/with_screen.csv'

df1 = pd.read_csv(spectra_1)
df2 = pd.read_csv(spectra_2)

df1 = df1[(df1['wavelengths'] >= 300) & (df1['wavelengths'] <= 800)]
df2 = df2[(df2['wavelengths'] >= 300) & (df2['wavelengths'] <= 800)]

ratio = df1['spectra'] / df2['spectra']

plt.plot(df1['wavelengths'], ratio)
plt.xlabel('Wavelengths (nm)')
plt.ylabel('Spectra Ratio')
plt.show()