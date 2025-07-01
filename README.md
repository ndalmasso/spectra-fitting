# spectral-line-fitting

## Overview

A Python tool for fitting emission lines in astronomical spectra with automatic doublet fitting and integrated flux calculations. Given source spectra and detected emission line wavelengths, the tool provides robust continuum fitting, line profile analysis, and comprehensive visualization capabilities for spectroscopic data analysis.

## "How to Fit a Spectra for Dummies"
Here's a simple step-by-step guide to analyze your spectral data:

### Step 1: Start with Your Data
You need a spectrum file with emission lines already identified. Load your `.txt` file containing wavelengths, flux values, and the positions of detected emission lines.

### Step 2: Visual Inspection
Plot your spectrum to see the big picture. Look at your emission lines and identify which ones you want to analyze.
<p align="center">
  <img src="https://github.com/user-attachments/assets/dca333af-9ad2-4be3-9990-6c9548003a59" alt="Spectra Overview" width="100%" />
</p>  

### Step 3: Zoom In
Focus on the spectral region around your emission line of interest. This helps you see the line shape and surrounding continuum clearly.

### Step 4: Define Continuum Regions
Choose regions on both sides of your emission line where you think the continuum (background) is "clean" - areas without other lines or features. These will be your maximum boundaries for continuum fitting.
<p align="center">
  <img src="https://github.com/user-attachments/assets/8ee7b5a4-8389-43c6-b933-11033edae2b5" alt="Region Zoom" width="45%" />
</p>  

### Step 5: Let the Code Work Its Magic
The tool performs Monte Carlo minimization, trying different continuum regions within your specified boundaries to find the best fit. This ensures robust continuum estimation even if your initial guess isn't perfect.
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
│   ├── example_spectrum_A.txt
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
- Integrated flux measurements with uncertainties
- Continuum level and slope in fitting region

**Visualizations:**
- Full spectrum overview
- Zoomed fitting region showing continuum and line components

## Usage

See `spectra_fit_analysis.ipynb` for a complete analysis example.

## Citation

If you use this tool in your research, please cite: [Citation details to be added]

## Contact

For questions about the code or methodology, contact [ndalmasso](mailto:nicolo.dalmasso1@gmail.com).

---

**Note**: This is a demonstration tool. For production analysis, ensure proper data validation, error handling, and parameter optimization for your specific dataset.
