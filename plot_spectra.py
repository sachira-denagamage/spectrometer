import pandas as pd
import matplotlib.pyplot as plt
import utilities

spectra = '/Users/sachira/Desktop/Code/spectrometer/projector-measurements/single_lens_no_screen.csv'

df = pd.read_csv(spectra)

utilities.plot_spectrum(df['spectra'], df['wavelengths'])