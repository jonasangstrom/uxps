import numpy as np
from numpy.testing import assert_allclose
from uxps.io_functions import read_multiplex
from uxps.model import (pseudo_voigt, svsc, Model, get_data_in_range,
                        create_n_refine_multiple)


def test_peak_area():
    """ test that peak area is always scale (and works)
    """
    x = np.arange(0, 100, step=0.01)
    n_tests = 100
    scales = np.linspace(1, 1000, n_tests)
    sigmas = np.arange(1, 10, n_tests)
    mus = np.arange(40, 60, n_tests)
    alphas = np.arange(0, 1, n_tests)
    for scale, sigma, mu, alpha in zip(scales, sigmas, mus, alphas):
        peak = pseudo_voigt(x, scale, sigma, mu, alpha)
        print(scale, sigma, mu, alpha)
        assert_allclose(np.sum(peak)*0.01, scale, 0.001)


def test_svsc():
    """ test that background goes from 0 to k and is k/2 at peak mean
    """
    x = np.arange(0, 100, step=0.1)
    n_tests = 100
    scales = np.linspace(1, 1000, n_tests)
    sigmas = np.arange(1, 10, n_tests)
    mus = np.arange(40, 60, n_tests)
    alphas = np.arange(0, 1, n_tests)
    ks = np.arange(0.01, 20, n_tests)
    for k, scale, sigma, mu, alpha in zip(ks, scales, sigmas, mus, alphas):
        peak = pseudo_voigt(x, scale, sigma, mu, alpha)
        background = svsc(k, x, peak)
        assert_allclose(background[0], 0, 0.001)
        assert_allclose(background[-1], k, 0.001)
        assert_allclose(background[np.argmax(peak)], k/2, 0.1)


def test_get_data_in_range():
    x = np.array([5, 10, 1, 100, 2, 101])
    y = np.array([1, 2, 3, 4, 5, 6])
    x, y = get_data_in_range(x, y, lower=5, upper=100)
    assert_allclose(x, np.array([5, 10, 100]), 0.001)
    assert_allclose(y, np.array([1, 2, 4]), 0.001)


def test_model_refine():
    path = 'multiplex.txt'
    mplx_dict = read_multiplex(path)
    c1s = mplx_dict['C 1s']
    peaknames = ['C-C 1s', 'O-C=O ?']
    mus = [286, 288.5]
    vary_mus = [False, True]
    x_shift = 3
    vary_x_shift = True
    sigmas = [1.5, 1.5]
    scales = [10000, 10000]
    ks = [0.0001, 0.0001]
    alpha = 0.5
    a0 = 1000
    a1 = 0
    x, y = get_data_in_range(c1s['x'], c1s['y'], 275, 298)

    model = Model(peaknames, mus, vary_mus, x_shift, vary_x_shift, sigmas,
                  scales, ks, alpha, a0, a1, x, y)

    model.fit()

    assert_allclose(model.pars['mu0'], 286, 0.00001)
    assert_allclose(model.pars['x_shift'], 3, 0.5)
    assert_allclose(model.pars['mu1'], 288.5, 0.1)


def test_create_n_refine_multiple_single():
    path = 'multiplex.txt'
    mplx_dict = read_multiplex(path)
    models_pars_list = [['C 1s', ['C-C 1s', 'O-C=O ?'], [286, 288.5], 275, 298]]
    models_dict = create_n_refine_multiple(models_pars_list, mplx_dict)
    model = models_dict['C 1s']

    assert_allclose(model.pars['mu0'], 286, 0.00001)
    assert_allclose(model.pars['x_shift'], 3, 0.5)
    assert_allclose(model.pars['mu1'], 288.5, 0.1)
