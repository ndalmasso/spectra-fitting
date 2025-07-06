# spectral-line-fitting

## Overview

A Python tool for fitting emission lines in astronomical spectra with automatic doublet fitting and integrated flux calculations. Given source spectra and detected emission line wavelengths, the tool provides robust continuum fitting, line profile analysis, and comprehensive visualization capabilities for spectroscopic data analysis.

## "How to Fit a Spectra for Dummies"
Here's a simple step-by-step guide to analyze your spectral data following the notebook "spectra_fit_analysis.ipynb".

### Step 1: Start with Your Data
You need a spectrum file with emission lines already identified. Load your `.txt` file containing wavelengths, flux values, and the positions of detected emission lines. (Two different spectra given in "/spectra" to play with)
```python
import numpy as np
import specfit

# Load and process spectrum data
data = np.loadtxt('example_spectrum_A.txt', skiprows=1)
obs_wave = data[:, 0]
obs_flux = data[:, 1] 
em_lines_all = data[:, 2]

# Normalize flux and extract valid emission lines
norm = 1e-19
obs_flux = obs_flux / norm
obs_em_lines_wave = em_lines_all[~np.isnan(em_lines_all)]

# Filter data to good wavelength ranges (dictated by instrumentation)
good_ranges = [(1.013e4, 1.283e4), (1.330e4, 1.671e4), (1.751e4, 2.226e4)]
wave_filter, flux_filter = specfit.ranges_filter(obs_wave, obs_flux, ranges=good_ranges)
```

### Step 2: Visual Inspection
Plot your spectrum to see the big picture. Look at your emission lines and identify which ones you want to analyze.
```python
# Plot entire spectrum
specfit.plot_spectrum(wave_filter, flux_filter, obs_em_lines_wave, norm)
```

<p align="center">
  <img src="https://github.com/user-attachments/assets/dca333af-9ad2-4be3-9990-6c9548003a59" alt="Spectra Overview" width="100%" />
</p>  

### Step 3: Zoom In and Define Continuum Ranges
Narrow your focus to the spectral region containing your emission line. This close-up view reveals the line's shape and the surrounding baseline. Next, identify "clean" regions on either side of the emission line—areas free from other spectral features where only the continuum is visible. Mark these as your boundary limits for continuum fitting.
```python
# Plot zoomed spectrum with continuum shading
mask = (wave_filter >= zoom_min) & (wave_filter <= zoom_max)
em_lines_in_range = obs_em_lines_wave[(obs_em_lines_wave >= zoom_min) & (obs_em_lines_wave <= zoom_max)]
wave_zoom = np.array(wave_filter[mask])
flux_zoom = np.array(flux_filter[mask])

print(f'Emission line(s) in zoom = {em_lines_in_range}')
specfit.plot_spectrum(wave_filter, flux_filter, obs_em_lines_wave, norm, 
                     zoom=zoom_range, cont=cont_range)
```
<p align="center">
  <img src="https://github.com/user-attachments/assets/8ee7b5a4-8389-43c6-b933-11033edae2b5" alt="Region Zoom" width="45%" />
</p>  

### Step 4: Let the Code Work Its Magic
The tool performs Monte Carlo minimization, trying different continuum regions within your specified boundaries to find the best fit. This ensures robust continuum estimation even if your initial guess isn't perfect.
```python
# Parameters
line_1, line_2 = 'line1', 'line2'
center_wave_1, center_wave_2 = 14182.74, 14320.02
n_iter = 1e3

# Automatic doublet detection and fitting
is_doublet = bool(line_1 and line_2 and center_wave_2)
result = specfit.em_line_fit(wave_zoom, flux_zoom, center_wave_1, center_wave_2, 
                            line_1, line_2, cont_range, zoom_range[0], n_iter)

# Unpack results based on doublet status
if is_doublet:
    continuum, xx_fit, fit1, fit2 = result
    fits = [fit1, fit2]
    labels = [line_1, line_2]
    colors = ['blue', 'orange']
else:
    continuum, xx_fit, fit1 = result
    fits = [fit1]
    labels = [line_1]
    colors = ['orange']

# Calculate integrated flux (using the fit you want to analyse)
integrated_flux, integrated_flux_error = specfit.calculate_line_flux(xx_fit, fit1, continuum, norm)

# Plot fitted spectrum
specfit.plot_fitted_spectrum(wave_filter, flux_filter, obs_em_lines_wave, norm, 
                           zoom_range, cont_range, xx_fit, continuum, 
                           fits, labels, colors)
```
<p align="center">
  <img src="https://github.com/user-attachments/assets/8adb477e-7249-4607-800b-ae1b5c4c8444" alt="Lines Fit" width="45%" />
</p>

### Bonus: Doublet Fitting
If you have two closely spaced lines (like a doublet), specify both line positions and the code will fit them simultaneously using the same continuum - giving you more accurate results for both lines.

**Key Features:**
* Single and doublet emission line fitting
* Automatic continuum minimization with Monte Carlo estimation
* Configurable analysis parameters
* Publication-quality plotting


## Data Format

The tool expects spectral data in `.txt` format with three columns:
- **Column 1**: Wavelength (Angstroms)
- **Column 2**: Flux density (arbitrary units)
- **Column 3**: Detected emission line wavelengths

## Repository Structure

```
├── spectra_fit_analysis.ipynb         # Analysis example
├── specfit.py                         # Core spectral fitting module
├── spectra/                           # Example spectrum files
│   ├── example_spectrum_A.txt         # Two example spectra to play with
│   └── example_spectrum_B.txt
└── README.md                          # This file
```

## Requirements

```python
numpy>=1.20.0
matplotlib>=3.3.0
scipy>=1.7.0
```

## Methods

The analysis employs:
- **Gaussian line profiles** for emission line modeling
- **Linear continuum fitting** in user-defined regions with Monte Carlo minimization
- **Automatic doublet detection** and simultaneous fitting
- **Error propagation** for integrated flux measurements

## Output

The tool generates:

**Fitted Parameters:**
- Central wavelength, FWHM, amplitude (extractable from `specfit.py` functions)
- Continuum level and slope in fitting region (extractable from `specfit.py` functions)
- Integrated flux measurements with uncertainties

## Citation

If you use this tool in your research, please cite: [PAPER]

## Contact

For questions about the code or methodology, contact [ndalmasso](mailto:nicolo.dalmasso1@gmail.com).

---

**Note**: This is a demonstration tool. For production analysis, ensure proper data validation, error handling, and parameter optimization for your specific dataset.
