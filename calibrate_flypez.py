import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import re

folderpath = '/Users/sachira/Desktop/Code/spectrometer/flypez-measurements/240426'
led_wavelengths = ['415', '455', '565', '617', 'white']
colors = ['violet','blue','green','orange','grey']
violet_y = None
x_values = []
x_values_dict = {}

for i in range(len(led_wavelengths)):
    flux_sum = []
    background  = pd.read_csv(folderpath + '/' + led_wavelengths[i] + 'nm_' + '0mA.csv')

    all_files = os.listdir(folderpath)
    led_files = [f for f in all_files if f.startswith(led_wavelengths[i] + 'nm_') and f.endswith('mA.csv')]
    led_intensities = [int(re.search(r'(\d+)mA.csv', f).group(1)) for f in led_files]
    led_intensities = [intensity for intensity in led_intensities if intensity != 0]
    led_intensities.sort()
    
    for intensity in led_intensities:  # loop over led_intensities
        led = pd.read_csv(folderpath+'/' + led_wavelengths[i] + 'nm_' + str(intensity) + 'mA.csv')
        led = led[(led['wavelengths'] >= 350) & (led['wavelengths'] <= 650)]
        flux = led['spectra'] - background['spectra']
        flux_sum.append(np.sum(np.maximum(flux, 0)))
    plt.scatter(led_intensities, flux_sum, color = colors[i])
    
    b, a = np.polyfit(led_intensities, flux_sum, deg=1)
    xseq = np.linspace(0, 1200, num=120)
    plt.plot(xseq, a + b * xseq, color = colors[i])

    if led_wavelengths[i] == 'white':
        if violet_y is not None:  # ensure violet_y is not None before subtraction
            x_value = (violet_y - a) / b  # x-value corresponding to violet_y
            x_values_dict[led_wavelengths[i]] = x_value
            x_values.append(x_value)
    elif int(led_wavelengths[i]) == 415:  # violet LED
        violet_y = a + b * 1000  # y-value at x = 1000
        plt.axhline(y=violet_y, color='violet', linestyle='--')  # draw horizontal dashed line
    else:
        if violet_y is not None:  # ensure violet_y is not None before subtraction
            x_value = (violet_y - a) / b  # x-value corresponding to violet_y
            x_values_dict[led_wavelengths[i]] = x_value
            x_values.append(x_value)
plt.xlabel('Current (mA)')
plt.ylabel('Photon flux (photon.cm-3.s-1)')
plt.show()

print("Photon flux for violet LED at current = 1000 mA: ", violet_y)
print("Current values for other LEDs corresponding to violet LED: ", x_values_dict)