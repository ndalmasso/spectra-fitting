import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from scipy.optimize import curve_fit
from matplotlib.ticker import MultipleLocator
import warnings
warnings.filterwarnings('ignore', module='matplotlib')

def ranges_filter(wave, flux, ranges):
    """Filter spectrum data to include only specified wavelength ranges."""
    if ranges:
        mask = np.zeros_like(wave, dtype=bool)
        for start, end in ranges:
            mask = mask | ((wave >= start) & (wave <= end))
        filter_wave = np.ma.array(wave, mask=~mask)
        filter_flux = np.ma.array(flux, mask=~mask)
        return filter_wave, filter_flux
    else:
        return wave, flux


def plot_spectrum(wave, flux, obs_em_lines_wave, norm, zoom=None, cont=None):
    """
    Plot spectrum with optional zoom functionality and continuum shading
    
    Parameters:
    wave, flux : arrays for spectrum data
    obs_em_lines_wave : array of emission line wavelengths
    norm : normalization factor for y-label
    zoom : list of tuples [(start, end)] for zoom regions, or None for full range
    cont : list of tuples [(start, end)] for continuum regions to shade, or None
    """
    figsize = (7, 7) if zoom else (21, 7)
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor('white')
    
    # Plot dummy lines for legend
    ax.plot(0, 0, linestyle='-', color='grey', alpha=1, label='spectra')
    ax.plot(0, 0, linestyle='--', color='m', alpha=1, label='em_lines')
    
    # Plot spectra
    ax.step(wave, flux, 'grey', alpha=1)
    
    # Plot observed emission lines
    for x in obs_em_lines_wave:
        ax.axvline(x=x, color='m', linestyle='--', linewidth=1)
    
    # Set labels and formatting
    ax.set_xlabel(r'$\lambda$ [$\AA$]', fontsize='xx-large')
    ax.set_ylabel(rf'$f_{{\lambda}}$ [$erg/s/cm^2/\AA$]$\cdot$ {norm:.0e}', fontsize='xx-large')
    ax.tick_params(axis='both', labelsize=15, size=10, which='major')
    ax.tick_params(axis='both', labelsize=15, size=4, which='minor')
    
    # Set axis limits based on zoom
    if zoom:
        x_min, x_max = zoom[0]
        ax.set_xlim(x_min, x_max)
        
        # Filter data for y-limit calculation
        mask = (wave >= x_min) & (wave <= x_max)
        if hasattr(flux, 'compressed'):  # Handle masked arrays
            flux_zoom = flux.compressed() if np.any(mask) else flux
            flux_in_range = flux_zoom[mask.compressed() if hasattr(mask, 'compressed') else mask]
        else:
            flux_in_range = flux[mask]
        
        if len(flux_in_range) > 0:
            ax.set_ylim(0, 1.2*max(flux_in_range))
        else:
            ax.set_ylim(0, 1.2*max(flux))
            
        # Adjust tick spacing for zoom
        range_width = x_max - x_min
        if range_width <= 2000:
            ax.xaxis.set_major_locator(MultipleLocator(500))
            ax.xaxis.set_minor_locator(MultipleLocator(100))
        else:
            ax.xaxis.set_major_locator(MultipleLocator(1000))
            ax.xaxis.set_minor_locator(MultipleLocator(250))
    else:
        # Default full range
        ax.set_xlim(1e4, 2.2e4)
        ax.xaxis.set_major_locator(MultipleLocator(2e3))
        ax.xaxis.set_minor_locator(MultipleLocator(0.5e3))
    
    ax.yaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_minor_locator(MultipleLocator(0.5))
    ax.grid(which='major', linestyle=':', alpha=0.5)
    ax.grid(which='minor', linestyle=':', alpha=0.5)
    
    # Add continuum shading if specified
    if cont:
        y_min, y_max = ax.get_ylim()
        y_range = y_max - y_min
        shade_height = 0.02 * y_range
        
        # Add legend entry for continuum regions
        ax.axvspan(0, 0, 
                  ymin=(y_min - shade_height - y_min)/y_range,
                  ymax=(y_min + shade_height - y_min)/y_range,
                  alpha=0.3, color='red', label='cont_regions')
        
        for continuum_range in cont:
            continuum_min, continuum_max = continuum_range
            ax.axvspan(continuum_min, continuum_max, 
                      ymin=(y_min - shade_height - y_min)/y_range,
                      ymax=(y_min + shade_height - y_min)/y_range,
                      alpha=0.3, color='red')
    
    ax.legend(loc='best', fontsize=14, frameon=True, handletextpad=0.4).get_frame().set_alpha(1)
    plt.show()
    
    
def em_line_fit(wave, flux, center_wavelength1, center_wavelength2, line1, line2, continuum_ranges, zoom_range, n_iter):
    """
    Fit emission lines with continuum estimation
    """
    
    def gaussian(x, amplitude, center, sigma):
        return amplitude * np.exp(-(x - center)**2 / (2 * sigma**2))

    def model_single(x, *params):
        background = line_cont(x, *pop_cont)
        return background + gaussian(x, *params)

    def line_cont(x, m, q):
        return x*m + q
    
    def sample_continuum_ranges(ranges):
        sampled = []
        for cont_min, cont_max in ranges:
            full_width = cont_max - cont_min
            min_width = 0.1 * full_width
            width = np.random.uniform(min_width, full_width)
            start = np.random.uniform(cont_min, cont_max - width)
            end = start + width
            sampled.append((round(start, 2), round(end, 2)))
        return sampled

    def calculate_continuum(wave_subset, flux_subset, continuum_ranges):
        # Collect wavelengths and fluxes within continuum ranges
        continuum_waves = []
        continuum_fluxes = []

        for cont_min, cont_max in continuum_ranges:
            cont_mask = (wave_subset >= cont_min) & (wave_subset <= cont_max)
            continuum_waves.extend(wave_subset[cont_mask])
            continuum_fluxes.extend(flux_subset[cont_mask])

        continuum_waves = np.array(continuum_waves)
        continuum_fluxes = np.array(continuum_fluxes)

        f_ = interpolate.interp1d(continuum_waves, continuum_fluxes)
        xx_fine = np.linspace(min(continuum_waves), max(continuum_waves), 500)
        flux_interp = f_(xx_fine)

        # Fit polynomial to continuum points
        popt_par, pcov_par = curve_fit(line_cont, xx_fine, flux_interp)
        return popt_par, pcov_par
    
    # Determine if fitting doublet or single line
    is_doublet = bool(line1 and line2)
        
    # Create interpolation grids
    xx_zoom = np.linspace(zoom_range[0], zoom_range[1], 500)
    xx_fine = np.linspace(min(wave), max(wave), 500)
    f_ = interpolate.interp1d(wave, flux)
    flux_interp = f_(xx_fine)
    
    # Monte Carlo continuum estimation
    cont, pcont_array = [], []
    
    for i in range(int(n_iter)):
        sampled_ranges = sample_continuum_ranges(continuum_ranges)
        try:
            popt_cont, _ = calculate_continuum(wave, f_(wave), sampled_ranges)
            continuum = line_cont(xx_fine, *popt_cont)
            cont.append(continuum)
            pcont_array.append(popt_cont)
        except Exception:
            continue
    
    # Calculate median continuum parameters
    cont_med = np.median(cont, axis=0)
    pop_cont = np.median(pcont_array, axis=0)

    if is_doublet:
        # Handle doublet fitting
        rang1 = abs(min([min(r) for r in continuum_ranges]) - center_wavelength1)
        rang2 = abs(max([max(r) for r in continuum_ranges]) - center_wavelength2)

        # Create symmetric flux arrays for each line
        idx_1 = xx_fine <= center_wavelength1
        idx_2 = xx_fine >= center_wavelength2
        flux_1 = np.concatenate([flux_interp[idx_1], np.flip(flux_interp[idx_1])])
        flux_2 = np.concatenate([np.flip(flux_interp[idx_2]), flux_interp[idx_2]])

        x_flip1 = np.linspace(center_wavelength1-rang1, center_wavelength1+rang1, len(flux_1))
        x_flip2 = np.linspace(center_wavelength2-rang2, center_wavelength2+rang2, len(flux_2))

        # Fit both lines
        p0_1 = [max(flux_1), center_wavelength1, 10]
        p0_2 = [max(flux_2), center_wavelength2, 10]

        popt_1, _ = curve_fit(model_single, x_flip1, flux_1, p0=p0_1)
        popt_2, _ = curve_fit(model_single, x_flip2, flux_2, p0=p0_2)

        fit_1 = model_single(xx_zoom, *popt_1)
        fit_2 = model_single(xx_zoom, *popt_2)
        
        return cont_med, xx_zoom, fit_1, fit_2

    else:
        # Handle single line fitting
        continuum_extremes = [item for sublist in continuum_ranges for item in sublist]
        rang1 = abs(min(continuum_extremes) - center_wavelength1)
        rang2 = abs(max(continuum_extremes) - center_wavelength1)

        # Create symmetric flux arrays
        idx_1 = xx_fine <= center_wavelength1
        idx_2 = xx_fine >= center_wavelength1
        flux_1 = np.concatenate([flux_interp[idx_1], np.flip(flux_interp[idx_1])])
        flux_2 = np.concatenate([np.flip(flux_interp[idx_2]), flux_interp[idx_2]])

        x_flip1 = np.linspace(center_wavelength1-rang1, center_wavelength1+rang1, len(flux_1))
        x_flip2 = np.linspace(center_wavelength1-rang2, center_wavelength1+rang2, len(flux_2))

        # Fit both sides and average
        p0_1 = [max(flux_1), center_wavelength1, 10]
        p0_2 = [max(flux_2), center_wavelength1, 10]

        popt_1, _ = curve_fit(model_single, x_flip1, flux_1, p0=p0_1)
        popt_2, _ = curve_fit(model_single, x_flip2, flux_2, p0=p0_2)

        fit_1 = model_single(xx_zoom, *popt_1)
        fit_2 = model_single(xx_zoom, *popt_2)
        fit_mean = (fit_1 + fit_2) / 2
        
        return cont_med, xx_zoom, fit_mean


def calculate_line_flux(xx_fine, fit, continuum, norm):
    """Calculate integrated line flux and error"""
    # Ensure arrays are numpy arrays
    xx_fine = np.array(xx_fine)
    fit = np.array(fit)
    
    if np.isscalar(continuum):
        continuum = np.full_like(fit, continuum)
    else:
        continuum = np.array(continuum)
    
    # Calculate integrated flux
    flux = np.trapz(fit - continuum, xx_fine)
    
    # Simple error estimation
    signal = fit - continuum
    variance = np.abs(signal) + np.abs(continuum)
    delta_wave = np.diff(xx_fine)[0]
    flux_error = np.sqrt(np.sum(variance) * delta_wave**2)
    
    return flux * norm, flux_error * norm
    
def plot_fitted_spectrum(wave_filter, flux_filter, obs_em_lines_wave, norm, zoom_range, 
                        cont_range, xx_fit, continuum, fits, labels, colors=None):
    """
    Plot spectrum with fitted emission lines
    
    Parameters:
    wave_filter, flux_filter : filtered spectrum data
    obs_em_lines_wave : emission line wavelengths
    norm : normalization factor
    zoom_range : zoom range as [(min, max)]
    cont_range : continuum regions
    xx_fit : x-axis for fitted lines
    continuum : continuum fit
    fits : list of fitted line profiles
    labels : list of line labels
    colors : list of colors for fits (optional)
    """
    if colors is None:
        colors = ['orange', 'blue']
    
    fig, ax = plt.subplots(figsize=(7, 7))
    fig.patch.set_facecolor('white')
    
    # Plot dummy lines for legend
    ax.plot(0, 0, linestyle='-', color='grey', alpha=1, label='spectra')
    ax.plot(0, 0, linestyle='--', color='m', alpha=1, label='em_lines')
    
    # Plot spectra
    ax.step(wave_filter, flux_filter, 'grey', alpha=1)
    
    # Plot observed emission lines
    for x in obs_em_lines_wave:
        ax.axvline(x=x, color='m', linestyle='--', linewidth=1)
    
    # Plot fitted lines
    for i, (fit, label) in enumerate(zip(fits, labels)):
        color = colors[i] if i < len(colors) else colors[0]
        ax.fill_between(xx_fit, continuum, fit, color=color, alpha=0.5, label=label)
    
    # Plot continuum
    ax.plot(xx_fit, continuum, 'k--', alpha=1, label='continuum')
    
    # Set labels and formatting
    ax.set_xlabel(r'$\lambda$ [$\AA$]', fontsize='xx-large')
    ax.set_ylabel(rf'$f_{{\lambda}}$ [$erg/s/cm^2/\AA$]$\cdot$ {norm:.0e}', fontsize='xx-large')
    ax.tick_params(axis='both', labelsize=15, size=10, which='major')
    ax.tick_params(axis='both', labelsize=15, size=4, which='minor')
    
    # Set axis limits
    x_min, x_max = zoom_range[0]
    ax.set_xlim(x_min, x_max)
    
    # Filter data for y-limit calculation
    mask = (wave_filter >= x_min) & (wave_filter <= x_max)
    if hasattr(flux_filter, 'compressed'):  # Handle masked arrays
        flux_zoom = flux_filter.compressed() if np.any(mask) else flux_filter
        flux_in_range = flux_zoom[mask.compressed() if hasattr(mask, 'compressed') else mask]
    else:
        flux_in_range = flux_filter[mask]
    
    if len(flux_in_range) > 0:
        ax.set_ylim(0, 1.2*max(flux_in_range))
    else:
        ax.set_ylim(0, 1.2*max(flux_filter))
    
    # Adjust tick spacing for zoom
    range_width = x_max - x_min
    if range_width <= 2000:
        ax.xaxis.set_major_locator(MultipleLocator(500))
        ax.xaxis.set_minor_locator(MultipleLocator(100))
    else:
        ax.xaxis.set_major_locator(MultipleLocator(1000))
        ax.xaxis.set_minor_locator(MultipleLocator(250))
    
    ax.yaxis.set_major_locator(MultipleLocator(1))
    ax.yaxis.set_minor_locator(MultipleLocator(0.5))
    ax.grid(which='major', linestyle=':', alpha=0.5)
    ax.grid(which='minor', linestyle=':', alpha=0.5)
    
    # Add continuum shading
    y_min, y_max = ax.get_ylim()
    y_range = y_max - y_min
    shade_height = 0.02 * y_range
    
    # Add legend entry for continuum regions
    ax.axvspan(0, 0, 
              ymin=(y_min - shade_height - y_min)/y_range,
              ymax=(y_min + shade_height - y_min)/y_range,
              alpha=0.3, color='red', label='cont_regions')
    
    for continuum_range in cont_range:
        continuum_min, continuum_max = continuum_range
        ax.axvspan(continuum_min, continuum_max, 
                  ymin=(y_min - shade_height - y_min)/y_range,
                  ymax=(y_min + shade_height - y_min)/y_range,
                  alpha=0.3, color='red')
    
    ax.legend(loc='best', fontsize=14, frameon=True, handletextpad=0.4).get_frame().set_alpha(1)
    plt.show()