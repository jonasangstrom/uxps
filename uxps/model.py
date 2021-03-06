import numpy as np
import lmfit as lm
from uxps.plotting import plot_refinement
from uxps.functions import get_data_in_range
from tqdm import tqdm


def pseudo_voigt(x, scale, sigma, mu, alpha):
    gaussian = np.exp(-(x-mu)**2/(2*sigma**2))/(sigma*np.sqrt(2*np.pi))
    lorentzian = (sigma/(np.pi*((x-mu)**2+sigma**2)))
    return scale * ((1-alpha) * gaussian + alpha * lorentzian)


def svsc(k, x_obs, peak):
    """ background https://onlinelibrary.wiley.com/doi/full/10.1002/sia.5453
    """
    dx = np.gradient(x_obs)
    return k*np.cumsum(dx*peak)


def diff(pars, x_obs, y_obs, model):
    y_calc, back, peaks = model(pars)
    return y_calc - y_obs


class Model:
    def __init__(self, peaknames, mus, vary_mus, x_shift, vary_x_shift,
                 sigmas, scales, ks, alpha, a0, a1, x_obs, y_obs, sweeps=1,
                 t_p_step=1):
        self.pars = lm.Parameters()
        for n, [mu, vary_mu, sigma, scale, k] in enumerate(zip(mus, vary_mus,
                                                               sigmas, scales,
                                                               ks)):
            self.pars.add('mu{}'.format(n), mu)
            self.pars['mu{}'.format(n)].vary = vary_mu
            self.pars.add('scale{}'.format(n), scale)
            self.pars['scale{}'.format(n)].min = 0
            self.pars.add('sigma{}'.format(n), sigma)
            self.pars['sigma{}'.format(n)].min = 0
            self.pars.add('k{}'.format(n), k)
            self.pars['k{}'.format(n)].min = 0
        self.pars.add('a0', a0)
        self.pars.add('a1', 0)
        self.pars['a1'].vary = False
        self.pars.add('x_shift', x_shift)
        self.pars['x_shift'].vary = vary_x_shift
        self.pars.add('alpha', alpha)
        self.pars['alpha'].min = 0.3
        self.pars['alpha'].max = 0.5
        self.pars['a0'].min = 0
        self.x_obs = x_obs
        self.y_obs = y_obs
        self.peaknames = peaknames
        self.sweeps = sweeps
        self.t_p_step = t_p_step

    def evaluate(self, pars):
        peaks = []
        back = pars['a0'] + pars['a1'] * self.x_obs
        for n, peakname in enumerate(self.peaknames):
            scale = pars['scale{}'.format(n)]
            sigma = pars['sigma{}'.format(n)]
            mu = pars['mu{}'.format(n)] + pars['x_shift']
            k = pars['k{}'.format(n)]
            alpha = pars['alpha']
            peaks.append(pseudo_voigt(self.x_obs, scale, sigma, mu, alpha))
            step = svsc(k, self.x_obs, peaks[n])
            back += step
        model = back.copy()
        for peak in peaks:
            model += peak
        return model, back, peaks

    def fit(self):
        result = lm.minimize(diff, self.pars, args=[self.x_obs, self.y_obs,
                                                    self.evaluate])
        self.pars = result.params

    def plot_refinement(self, colors, title, folder, show_plots):
        y_calc, back, peaks = self.evaluate(self.pars)
        x = self.x_obs - self.pars['x_shift']
        residual = diff(self.pars, x, self.y_obs, self.evaluate)
        plot_refinement(x, self.y_obs, y_calc, back, peaks, colors,
                        self.peaknames, x.min(), x.max(), title, residual,
                        folder, show_plots)

    def integrate_peak(self, peakname_to_inte):
        model, back, peaks = self.evaluate(self.pars)
        peak_dict = {peakname: peak for peakname, peak in zip(self.peaknames,
                                                              peaks)}
        peak_to_inte = peak_dict[peakname_to_inte]
        return np.sum(peak_to_inte)


def create_n_refine_multiple(models_pars_list, mplx_dict, x_shift=0, sigma=1.5,
                             scale=10000, k=0.0001, alpha=0.5, a0=1000,
                             a1=0, use_survey=False):
    """ Creates and refines multiple models, parameters are given as
    model_pars_list. Refines and then returns the refined models as a
    dictionary. Assumes that the first peak in the first model is used
    for zeros shift correction. The names in the multiplex and list must
    match. TODO: Change to either use either multiplex or survey.
    """
    models_dict = {}
    first = True
    for name, peaknames, mus, x_min, x_max in tqdm(models_pars_list):
        vary_mus = [True for mu in mus]
        sigmas = [sigma for mu in mus]
        scales = [scale, scale]
        ks = [k, k]

        if first:
            vary_x_shift = True
            vary_mus[0] = False
        else:
            vary_x_shift = False

        if use_survey:
            x = mplx_dict['x']
            y = mplx_dict['y']
        else:
            x = mplx_dict[name]['x']
            y = mplx_dict[name]['y']

        x, y = get_data_in_range(x, y, x_min+x_shift, x_max+x_shift)

        models_dict[name] = Model(peaknames, mus, vary_mus, x_shift,
                                  vary_x_shift, sigmas, scales, ks, alpha, a0,
                                  a1, x, y, mplx_dict[name]['sweeps'],
                                  mplx_dict[name]['t/step'])

        models_dict[name].fit()

        if first:
            x_shift = models_dict[name].pars['x_shift']
            first = False

    return models_dict
