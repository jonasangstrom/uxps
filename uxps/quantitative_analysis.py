import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def peak_to_n(model, orbital, x_section, peak_names):
    area = 0
    sweeps = model.sweeps
    t_p_step = model.t_p_step
    for peak_name in peak_names:
        area += model.integrate_peak(peak_name)
    return area/(x_section[orbital] * t_p_step * sweeps)


def peaks_to_n(models, peaks, x_section):
    """ Calculates n (peak area normalized by cross section sweeps and time
    per step) from list of peaks and models
    """
    n_dict = {}
    for peak in peaks:
        element, atomic_orbital, modeL_name, peak_names = peak
        n_dict[element] = peak_to_n(models[modeL_name], element+atomic_orbital,
                                    x_section, peak_names)
    return n_dict


def n_to_c(n_dict):
    """ Calculates concentrations (c) from normalized peak areas (n)
    """
    n_tot = 0
    for element in n_dict:
        n_tot += n_dict[element]
    return {element: n_dict[element]/n_tot for element in n_dict}


def peak_to_c(models, peaks, x_section):
    n_dict = peaks_to_n(models, peaks, x_section)
    return n_to_c(n_dict)


def plot_compositions(df, color_dict):
    ''' Takes a pandas dataframe df with element on columns and sample
    names as rownames
    '''
    fig, ax = plt.subplots(figsize=(9, 5))
    starts = np.zeros(df.shape[0])

    for element in df:
        values = df[element].values * 100
        samples = list(df.index)
        color = color_dict[element]
        if values.sum() > 0:
            ax.barh(samples, values, left=starts, height=0.5,
                    label=element, color=color)

        xcenters = starts + values / 2
        starts += values
        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'

        for y, (x, c) in enumerate(zip(xcenters, values)):
            if np.round(c) >= 2:
                ax.text(x, y, "{:2.0f}".format(c), ha='center', va='center',
                        color=text_color)
                ax.legend(ncol=df.shape[1], bbox_to_anchor=(0, 1),
                          loc='lower left', fontsize='small')

    ax.set_xlabel('at%')
    ax.set_xlim(0, 100)
    plt.tight_layout()
    plt.show()


def create_select_elements(include_elements, original_df, typ, names):
    """ Create a new pandas dataframe with all compositions except the ones
    given are set to 0 and the others normalized to sum to 1.
    """
    df = original_df.copy()
    elements = np.array(df.columns)
    mask = np.zeros_like(elements, dtype=bool)
    for element in include_elements:
        mask += (elements == element)

    df = df.T
    for name in names:
        df[name+typ] = df[name] * mask
        df[name+typ] = df[name+typ]/df[name+typ].sum()
    return df.T


def generate_color_dict(df, cmap):
    """ Generate the colordict to assign a color to a specific element
    """
    category_colors = plt.get_cmap(cmap)(np.linspace(0.0, 1.0, df.shape[1]))
    return {element: color for color, element in zip(category_colors, df)}
