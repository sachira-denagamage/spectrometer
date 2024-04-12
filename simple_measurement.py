import utilities
import os
import pandas as pd
import matplotlib.pyplot as plt

params = {
    'acq_delay': 400,  # uS
    'integration_time': 1000000,  # uS
    'scans_to_average': 10,
    'boxcar_width': 5,
    'electric_dark_correction_usage': True,
    'nonlinearity_correction_usage': True
}

cal_filepath = '/Users/sachira/Desktop/Code/spectrometer/calibration-files/SR401083_cc_20240322.IRRADCAL'
save_dir = '/Users/sachira/Desktop/Code/spectrometer/projector-measurements'
measurement_name = 'test'

device = utilities.open_device()
serialNumber = device.get_serial_number()

print("Opening device!\n")
print("Serial Number: %s     \n" % serialNumber)

calibration = utilities.read_calibration_file(cal_filepath)
utilities.set_acquisition_parameters(device, params)

input("Ready for background? Press any key when ready.")
background_spectra, _ = utilities.take_measurement(device, calibration)
input("Ready for measurement? Press any key when ready.")
spectra, wavelengths = utilities.take_measurement(device, calibration)
spectra = spectra - background_spectra
filename = f"{measurement_name}.csv"
df = pd.DataFrame({'wavelengths': wavelengths, 'spectra': spectra})
df.to_csv(os.path.join(save_dir, filename), index=False)

utilities.plot_spectrum(spectra, wavelengths)

print("Closing device!\n")
utilities.close_device