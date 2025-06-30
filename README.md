# spectral-line-fitting

## Overview
This repository contains a Python tool for fitting emission lines in astronomical spectra with automatic doublet detection and integrated flux calculations. The tool provides robust continuum fitting, line profile analysis, and comprehensive visualization capabilities for spectroscopic data analysis.

The implementation includes support for:
* Single and doublet emission line fitting
* Automatic continuum determination
* Bootstrap error estimation
* Configurable analysis parameters
* Publication-quality plotting

## Data Description

The tool expects spectral data in ASCII format with the following structure:
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
- **Linear continuum fitting** in user-defined regions
- **Bootstrap resampling** for uncertainty quantification and continuum optimization

### Key Features
- Automatic doublet detection and simultaneous fitting
- Flexible continuum region definition
- Integrated flux measurements with error propagation

## Output

The analysis produces:

- **Fitted line parameters**: Central wavelength, FWHM, amplitude
- **Integrated flux measurements**: Line flux and uncertainties
- **Continuum characteristics**: Level and slope in fitting region
- **Quality metrics**: Reduced χ², fitting residuals
- **Visualization plots**:
  - Full spectrum overview with emission lines marked
  - Zoomed fitting region with continuum and line components
  - Residual plots and uncertainty estimates

<p align="center">
  <img src="https://via.placeholder.com/400x300?text=Full+Spectrum" alt="Full Spectrum" width="45%" />
  <img src="https://via.placeholder.com/400x300?text=Line+Fitting" alt="Line Fitting Results" width="45%" />
</p>

## Error Handling

The tool includes comprehensive error handling for:
- Missing or corrupted data files
- Invalid wavelength ranges
- Convergence failures in fitting
- Insufficient data points in analysis regions

## Performance

Typical analysis times:
- Single line fitting: < 1 second
- Doublet fitting: < 5 seconds
- Bootstrap uncertainty estimation: 10-30 seconds (depending on iterations)

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Citations

If you use this tool in your research, please cite:


## Contact
For questions about the code or methodology, please contact [your.email@institution.edu].

**Note**: This tool is designed for astronomical spectroscopy applications. For other domains, parameter ranges and fitting models may need adjustment.
