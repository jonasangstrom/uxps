
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
    return mplx_dict


def get_properties(line):
    r_n, _, _, r_t, r_s, _, r_e, _, _ = [value.split() for value in
                                         line.split(';')]
    name = '{} {}'.format(r_n[-2], r_n[-1])
    t_p_step = int(r_t[-1])
    sweeps = int(r_s[-1])
    energy = float(r_e[-1])
    return name, t_p_step, sweeps, energy



