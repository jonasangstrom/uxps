import numpy as np
import pandas as pd
from uxps.model import get_data_in_range

# TODO create function to generate detail from survey

def read_multiplex(path):
    with open(path, 'r') as mplxfile:
        data = mplxfile.readlines()
    mplx_dict = {}
    data_started = False
    current_orbital = ''
    for line in data:
        new_orbital = (line[0:7] == 'Element')
        if new_orbital:
            current_orbital, t_p_step, sweeps, energy = get_properties(line)
            mplx_dict[current_orbital] = {}
            mplx_dict[current_orbital]['t/step'] = t_p_step
            mplx_dict[current_orbital]['sweeps'] = sweeps
            mplx_dict[current_orbital]['energy'] = energy
            mplx_dict[current_orbital]['x'] = []
            mplx_dict[current_orbital]['y'] = []
            data_started = True
        elif data_started and (len(line) > 1):
            x, y = line.split()
            mplx_dict[current_orbital]['x'].append(float(x))
            mplx_dict[current_orbital]['y'].append(float(y))
    for orbital in mplx_dict:
        mplx_dict[orbital]['x'] = np.array(mplx_dict[orbital]['x'])
        mplx_dict[orbital]['y'] = np.array(mplx_dict[orbital]['y'])
    return mplx_dict


def get_properties(line):
    r_n, _, _, r_t, r_s, _, r_e, _, _ = [value.split() for value in
                                         line.split(';')]
    name = ''
    for name_part in r_n[1:]:
        name += (name_part+' ')
    name = name[:-1]

    t_p_step = int(r_t[-1])
    sweeps = int(r_s[-1])
    energy = float(r_e[-1])
    return name, t_p_step, sweeps, energy


def list_to_array(a_list, sep='\t', dtype=float):
    return np.array([line.split(sep) for line in a_list], dtype=dtype)


def append_to_multiplex(survey_dict, mplx_dict, detail_name, start, end):
    """ Appends detail from survey dictionary file to multiplex dictionary
    """

    detail_dict = {}

    # copy details
    detail_dict['t/step'] = survey_dict['t/step']
    detail_dict['sweeps'] = survey_dict['sweeps']

    # copy x y data
    detail_dict['x'], detail_dict['y'] = get_data_in_range(survey_dict['x'],
                                                           survey_dict['y'],
                                                           start, end)
    mplx_dict[detail_name] = detail_dict

    return mplx_dict


def read_survey(path):
    with open(path, 'r') as a_file:
        content = a_file.readlines()
        name, t_p_step, sweeps, energy = get_properties(content[0])
        data = list_to_array(content[3:])
    survey_dict = {}
    survey_dict['t/step'] = t_p_step
    survey_dict['sweeps'] = sweeps
    survey_dict['energy'] = energy
    survey_dict['x'] = data[:, 0]
    survey_dict['y'] = data[:, 1]
    return survey_dict


def save_as_h5(c_dict, name, key):
    c_data_frame = pd.DataFrame.from_dict({element: [c_dict[element]] for
                                           element in c_dict})
    c_data_frame.to_hdf(name, key)
