from uxps.io_functions import (read_multiplex, get_properties, read_survey,
                               append_to_multiplex)
from uxps.functions import check_or_create_folder
from numpy.testing import assert_allclose
import os


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


def test_get_properties_no_name():
    line = """Element ; Region 1 of 10; Depth Cycle 1 of 1; Time Per Step
    100; Sweeps 15; Anode Al; Photon Energy 1486.6; XPS;"""
    name, t_p_step, sweeps, energy = get_properties(line)
    assert name == ''
    assert t_p_step == 100
    assert sweeps == 15
    assert_allclose(energy, 1486.6, rtol=0.00001)


def test_get_properties_one_name():
    line = """Element asdf; Region 1 of 10; Depth Cycle 1 of 1; Time Per Step
    100; Sweeps 15; Anode Al; Photon Energy 1486.6; XPS;"""
    name, t_p_step, sweeps, energy = get_properties(line)
    assert name == 'asdf'
    assert t_p_step == 100
    assert sweeps == 15
    assert_allclose(energy, 1486.6, rtol=0.00001)


def test_read_survey():
    path = 'survey.txt'
    survey_dict = read_survey(path)
    assert_allclose(survey_dict['x'][0], 1400, rtol=0.00001)
    assert_allclose(survey_dict['y'][0], 3252, rtol=0.00001)
    assert survey_dict['t/step'] == 100
    assert survey_dict['sweeps'] == 1
    assert_allclose(survey_dict['energy'], 1486.6, rtol=0.00001)


def test_append_detail_to_multiplex():
    path = 'survey.txt'
    survey_dict = read_survey(path)
    path = 'multiplex.txt'
    mplx_dict = read_multiplex(path)
    start = 1276.4
    end = 1349.2
    detail_name = 'asdf'
    mplx_dict = append_to_multiplex(survey_dict, mplx_dict, detail_name, start,
                                    end)
    detail_dict = mplx_dict[detail_name]
    assert detail_dict['t/step'] == 100
    assert detail_dict['sweeps'] == 1
    assert_allclose(detail_dict['x'][0], 1349.2, rtol=0.00001)
    assert_allclose(detail_dict['x'][-1], 1276.4, rtol=0.00001)
    assert_allclose(detail_dict['y'][0], 2638, rtol=0.00001)
    assert_allclose(detail_dict['y'][-1], 2646, rtol=0.00001)


def test_create_folder():
    path_to_folder = 'existing_folder/'
    check_or_create_folder(path_to_folder)
    assert os.path.isdir(path_to_folder)

    path_to_folder = 'existing_folder'
    check_or_create_folder(path_to_folder)
    assert os.path.isdir(path_to_folder)

    path_to_folder = 'nonexisting_folder/'
    check_or_create_folder(path_to_folder)
    assert os.path.isdir(path_to_folder)

    # cleanup
    os.rmdir(path_to_folder)
    assert not os.path.isdir(path_to_folder)
