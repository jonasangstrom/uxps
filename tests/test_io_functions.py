from uxps.io_functions import read_multiplex, get_properties, read_survey
from numpy.testing import assert_allclose


def test_read_multiplex():
    path = 'multiplex.txt'
    mplx_dict = read_multiplex(path)
    # check if 1st multiplex val OK
    na1s = mplx_dict['Na 1s']
    assert na1s['t/step'] == 100
    assert na1s['sweeps'] == 15
    assert_allclose(na1s['energy'], 1486.6, rtol=0.00001)
    assert_allclose(na1s['x'][0], 1086, rtol=0.00001)
    assert_allclose(na1s['y'][0], 3947, rtol=0.00001)
    # check if last multiplex val OK
    o1s = mplx_dict['O 1s']
    assert o1s['t/step'] == 100
    assert o1s['sweeps'] == 8
    assert_allclose(o1s['energy'], 1486.6, rtol=0.00001)
    assert_allclose(o1s['x'][0], 545, rtol=0.00001)
    assert_allclose(o1s['y'][0], 1290, rtol=0.00001)


def test_get_properties():
    line = """Element Na 1s; Region 1 of 10; Depth Cycle 1 of 1; Time Per Step
    100; Sweeps 15; Anode Al; Photon Energy 1486.6; XPS;"""
    name, t_p_step, sweeps, energy = get_properties(line)
    assert name == 'Na 1s'
    assert t_p_step == 100
    assert sweeps == 15
    assert_allclose(energy, 1486.6, rtol=0.00001)


def test_read_survey():
    path = 'survey.txt'
    survey_data = read_survey(path)
    assert_allclose(survey_data['x'][0], 1400, rtol=0.00001)
    assert_allclose(survey_data['y'][0], 3252, rtol=0.00001)
