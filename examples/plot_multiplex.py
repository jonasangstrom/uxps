import matplotlib.pyplot as plt
from uxps.io_functions import read_multiplex
from uxps.plotting import plot_detail
from uxps.model import Model, get_data_in_range

path = 'multiplex.txt'
mplx_dict = read_multiplex(path)
model_dict = {}
#test

def plot_scaled_multiplex(mplx_dict, model_dict, offset_name=''):
    # TODO plot refinements if avaliable and also plot survey
    for name in mplx_dict:
        detail = mplx_dict[name]
        t = detail['t/step'] * detail['sweeps']
        plot_detail(detail, name, scale=t,)
    plt.legend()
    plt.title('scaled multiplex+survey')
    plt.xlim(1000, 0)


plot_scaled_multiplex(mplx_dict, model_dict)
plt.show()
