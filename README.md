# spectral-line-fitting

## Overview
This repository contains a Python tool for fitting emission lines in astronomical spectra with automatic doublet fitting and integrated flux calculations. Having the the source spectra and the wavelength of the detected emission lines the he tool provides robust continuum fitting, line profile analysis, and comprehensive visualization capabilities for spectroscopic data analysis.

The implementation includes support for:
* Single and doublet emission line fitting
* Automatic continuum minimisation with MC estimation
* Configurable analysis parameters
* Publication-quality plotting

## Data Description

The tool expects spectral data in ".txt" format with the following structure:
- **Column 1**: Wavelength (Angstroms)
- **Column 2**: Flux density (arbitrary units)
- **Column 3**: Detected emission line wavelengths

## Repository Structure

```
├── spectra_fit_analysis.ipynb         # Example of analysis
├── specfit.py                         # Core spectral fitting module
├── spectra/                           # Example spectrum files
│   └── example_spectrum_A.txt         # Two example spectra to play with
│   └── example_spectrum_B.txt
└── README.md                           # This file
```

## Requirements

### Python Dependencies
```
numpy>=1.20.0
matplotlib>=3.3.0
scipy>=1.7.0
```

### Custom Module
- `specfit`: Contains emission line fitting algorithms, continuum estimation, and visualization tools

## Methods

### Emission Line Fitting
The analysis uses:
- **Gaussian line profiles** for emission line modeling
- **Linear continuum fitting** in user-defined regions with MC minimisation

### Key Features
- Automatic doublet simultaneous fitting
- Flexible continuum region definition with MC minimisation
- Integrated flux measurements with error propagation

## Output

The analysis produces:

- **Fitted line parameters**: Central wavelength, FWHM, amplitude
- **Integrated flux measurements**: Line flux and uncertainties
- **Continuum characteristics**: Level and slope in fitting region
- **Visualization plots**:
  - Full spectrum overview with emission lines marked
  - Zoomed fitting region with continuum and line components
  - Residual plots and uncertainty estimates

## Citations

If you use this tool in your research, please cite:


## Contact
For questions about the code or methodology, please contact [ndalmasso](nicolo.dalmasso1@gmail.com).

**Note**: This is a demonstration example. For production analysis, ensure proper data validation, error handling, and parameter optimization for your specific dataset.
