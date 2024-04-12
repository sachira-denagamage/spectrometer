import sys
sys.path.insert(1,'/Applications/OceanInsight/OceanDirect/python')
from oceandirect.OceanDirectAPI import OceanDirectAPI, OceanDirectError, FeatureID # type: ignore
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def open_device():
    od = OceanDirectAPI()
    device_count = od.find_usb_devices()
    device_ids = od.get_device_ids()
    id = device_ids[0]
    device = od.open_device(id)
    return device

def close_device():
    od = OceanDirectAPI()
    device_count = od.find_usb_devices()
    device_ids = od.get_device_ids()
    id = device_ids[0]
    od.close_device(id)

def set_acquisition_parameters(device, params):
    device.set_scans_to_average(params['scans_to_average'])
    device.set_acquisition_delay(params['acq_delay'])
    device.set_integration_time(params['integration_time'])
    device.set_boxcar_width(params['boxcar_width'])
    device.set_electric_dark_correction_usage(params['electric_dark_correction_usage'])
    device.set_nonlinearity_correction_usage(params['nonlinearity_correction_usage'])

def take_measurement(device, calibration):
    signal = device.get_formatted_spectrum()
    wavelengths = device.get_wavelengths()
    if not np.array_equal(np.round(np.array(wavelengths), 1), np.round(calibration['wavelengths'].to_numpy(), 1)):
        raise ValueError("Wavelengths from device do not match wavelengths from calibration file")

    integration_time = device.get_integration_time()/(10**6) #microseconds -> seconds
    area = 0.11946/(10**4) #cm^2 to m^2
    spectra = signal / (np.gradient(wavelengths)) #normalize to nM spacing between measurements
    spectra = spectra * calibration['calibration_values'].to_numpy() #uJ
    spectra = spectra / (integration_time * area) #uJ to uW/m^2
    spectra = spectra / 10**6 #uW/m^2 to W/m^2
    spectra = spectra * np.array(wavelengths) * 0.836 * 10**-2 #W/m^2 to uE
    return spectra, wavelengths

def read_calibration_file(cal_filepath):
    calibration = pd.read_csv(cal_filepath, sep='\t', header=None, skiprows=9)
    calibration.columns = ['wavelengths', 'calibration_values']

    return calibration

def plot_spectrum(spectra, wavelengths):
    plt.plot(wavelengths, spectra)
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Flux (uE)')
    plt.show()