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

## Usage

### Basic Analysis
```bash
python spectrum_analyzer.py --input data/spectra/example_spectrum_A.txt
```

### With Custom Configuration
```bash
python spectrum_analyzer.py --config config/my_analysis.json
```

### Python API
```python
from spectrum_analyzer import SpectrumAnalyzer

# Load configuration
config = {
    "good_ranges": [[10130, 12830], [13300, 16710], [17510, 22260]],
    "zoom_range": [[14000, 15000]],
    "continuum_range": [[14000, 14100], [14500, 15000]],
    "line_parameters": {
        "line_1": "H_alpha",
        "center_wave_1": 14182.74,
        "line_2": "H_beta", 
        "center_wave_2": 14320.02,
        "n_iterations": 1000
    }
}

# Analyze spectrum
analyzer = SpectrumAnalyzer(config)
analyzer.load_spectrum("data/spectra/example_spectrum_A.txt")
analyzer.filter_spectrum()
analyzer.run_analysis()
```

## Methods

### Emission Line Fitting
The analysis uses:
- **Gaussian line profiles** for emission line modeling
- **Linear continuum fitting** in user-defined regions
- **Levenberg-Marquardt optimization** for parameter estimation
- **Bootstrap resampling** for uncertainty quantification

### Key Features
- Automatic doublet detection and simultaneous fitting
- Flexible continuum region definition
- Integrated flux measurements with error propagation
- Quality control and outlier detection

## Configuration

Analysis parameters can be specified in JSON format:

```json
{
    "normalization": 1e-19,
    "good_ranges": [[10130, 12830], [13300, 16710], [17510, 22260]],
    "zoom_range": [[14000, 15000]],
    "continuum_range": [[14000, 14100], [14500, 15000]],
    "line_parameters": {
        "line_1": "emission_line_1",
        "center_wave_1": 14182.74,
        "line_2": "emission_line_2",
        "center_wave_2": 14320.02,
        "n_iterations": 1000
    }
}
```

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
```
@software{spectral_line_fitting,
  author = {Your Name},
  title = {Spectral Line Fitting Tool},
  url = {https://github.com/yourusername/spectral-line-fitting},
  year = {2025}
}
```

## Contact
For questions about the code or methodology, please contact [your.email@institution.edu].

**Note**: This tool is designed for astronomical spectroscopy applications. For other domains, parameter ranges and fitting models may need adjustment.
