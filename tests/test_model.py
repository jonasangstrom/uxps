import numpy as np
from numpy.testing import assert_allclose
from uxps.model import pseudo_voigt, svsc


def test_peak_area():
    """test that peak area is always scale (and works)
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
