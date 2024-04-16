import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import utilities

def led_measurement(device, calibration, led_wavelength, max_current):
    for current in range(0, max_current + 1, 100):
        ready = ''
        while ready.lower() != 'y':
            ready = input("Ready for measurement at current {}mA? y/n ".format(current))

        spectra, wavelengths = utilities.take_measurement(device, calibration)
            
        df = pd.DataFrame({
            'wavelengths': wavelengths,
            'spectra': spectra
        })

        dir_path = "/Users/sachira/Desktop/Code/spectrometer/flypez-measurements"
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            
        date_str = datetime.now().strftime("%y%m%d")
        sub_dir_path = os.path.join(dir_path, date_str)
        if not os.path.exists(sub_dir_path):
            os.makedirs(sub_dir_path)

        filename = f"{led_wavelength}nm_{current}mA.csv"
        df.to_csv(os.path.join(sub_dir_path, filename), index=False)

def plot_spectra(led_wavelength, max_current):
    date_str = datetime.now().strftime("%y%m%d")
    dir_path = "/Users/sachira/Desktop/Code/spectrometer/flypez-measurements"
    sub_dir_path = os.path.join(dir_path, date_str)

    background_df = pd.read_csv(os.path.join(sub_dir_path, f"{led_wavelength}nm_0mA.csv"))
    background_spectra = background_df['spectra']

    fig, axs = plt.subplots(2)

    for current in range(100, max_current + 1, 100):
        df = pd.read_csv(os.path.join(sub_dir_path, f"{led_wavelength}nm_{current}mA.csv"))
        spectra = df['spectra']

        spectra = spectra - background_spectra

        mask = (df['wavelengths'] >= 300) & (df['wavelengths'] <= 800)
        wavelengths = df['wavelengths'][mask]
        spectra = spectra[mask]

        axs[0].plot(wavelengths, spectra, label=f"{current}mA")

        integrated_flux = np.cumsum(spectra)

        axs[1].plot(wavelengths, integrated_flux, label=f"{current}mA")

    axs[0].legend()
    axs[1].legend()

    plt.savefig(os.path.join(sub_dir_path, f"{led_wavelength}nm_spectra.png"))

    plt.show()

params = {
    'acq_delay': 400,  # uS
    'integration_time': 1000000,  # uS 10000000
    'scans_to_average': 5,
    'boxcar_width': 5,
    'electric_dark_correction_usage': True,
    'nonlinearity_correction_usage': True
}

cal_filepath = '/Users/sachira/Desktop/Code/spectrometer/calibration-files/SR401083_cc_20240322.IRRADCAL'

device = utilities.open_device()
serialNumber = device.get_serial_number()

print("Opening device!\n")
print("Serial Number: %s     \n" % serialNumber)

calibration = utilities.read_calibration_file(cal_filepath)
utilities.set_acquisition_parameters(device, params)

led_wavelength = input("Enter the wavelength of the LED: ")
max_current = int(input("Enter the maximum current of the LED: "))

led_measurement(device, calibration, led_wavelength, max_current)

plot_spectra(led_wavelength, max_current)

print("Closing device!\n")
utilities.close_device