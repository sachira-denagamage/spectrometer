import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import utilities
import os

def take_grid_measurement(device, num_rows, num_columns, led_wavelengths, calibration, save_dir):
    intensities_dict = {}

    input("Ready for background? Press any key when ready.")
    background_spectra, _ = utilities.take_measurement(device, calibration)

    for i in range(num_rows):
        for j in range(num_columns):
            while True:
                confirmation = input("Is the spectrometer positioned at ({}, {})? y/n: ".format(i, j))
                if confirmation.lower() == 'y':
                    break

            spectra, wavelengths = utilities.take_measurement(device,calibration)

            spectra = spectra - background_spectra

            df = pd.DataFrame({'wavelengths': wavelengths, 'spectra': spectra})
            df.to_csv(os.path.join(save_dir, f'spectra_{i}_{j}.csv'), index=False)

            if i == 0 and j == 0:
                utilities.plot_spectrum(spectra, wavelengths)
                good_spectrum = input("Does the spectrum look good? y/n: ")
                if good_spectrum.lower() != 'y':
                    return

            wavelengths = np.array(wavelengths)

            for led_wavelength in led_wavelengths:
                #find maximum within 10nm of specified led_wavelength
                close_indices = np.where((wavelengths >= led_wavelength - 10) & (wavelengths <= led_wavelength + 10))[0]
                led_index = close_indices[np.argmax(spectra[close_indices])]

                if led_wavelength not in intensities_dict:
                    intensities_dict[led_wavelength] = [[0 for _ in range(num_columns)] for _ in range(num_rows)]

                intensities_dict[led_wavelength][i][j] = spectra[led_index]

    return intensities_dict

def plot_intensities(intensities_dict, save_dir):
    for led_wavelength, intensities in intensities_dict.items():
        intensities = np.array(intensities)
        mean_intensity = np.mean(intensities)
        percent_diff = (intensities - mean_intensity) / mean_intensity * 100

        fig, axs = plt.subplots(2, 1, figsize=(10, 10))

        sns.heatmap(intensities, cmap="vlag", annot=True, fmt=".2f", ax=axs[0])
        axs[0].set_xlabel('Column')
        axs[0].set_ylabel('Row')
        axs[0].set_title(f'Flux Heatmap (uE) for {led_wavelength}nm')

        sns.heatmap(percent_diff, cmap="vlag", annot=True, fmt=".1f", ax=axs[1])
        axs[1].set_xlabel('Column')
        axs[1].set_ylabel('Row')
        axs[1].set_title(f'Flux Heatmap (% Difference from Mean) for {led_wavelength}nm')

        plt.tight_layout()

        # Save the figure
        fig_name = f"Flux_Heatmap_{led_wavelength}nm.png"
        fig_path = os.path.join(save_dir, fig_name)
        plt.savefig(fig_path)

        plt.close(fig)

params = {
    'acq_delay': 400,  # uS
    'integration_time': 100000,  # uS
    'scans_to_average': 10,
    'boxcar_width': 5,
    'electric_dark_correction_usage': True,
    'nonlinearity_correction_usage': True
}

save_dir = '/Users/sachira/Desktop/Code/spectrometer/projector-measurements'

num_rows = 7
num_columns = 11
led_wavelength = [375,415,455,565,617] #list of wavelengths in nm

cal_filepath = '/Users/sachira/Desktop/Code/spectrometer/calibration-files/SR401083_cc_20240322.IRRADCAL'
calibration = utilities.read_calibration_file(cal_filepath)

device = utilities.open_device()
serialNumber = device.get_serial_number()

print("Opening device!\n")
print("Serial Number: %s     \n" % serialNumber)

utilities.set_acquisition_parameters(device, params)
intensities = take_grid_measurement(device, num_rows, num_columns, led_wavelength, calibration, save_dir)

plot_intensities(intensities, save_dir)

print("Closing device!\n")
utilities.close_device()
