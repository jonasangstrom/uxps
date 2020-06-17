import matplotlib.pyplot as plt
from uxps.io_functions import read_multiplex
from uxps.plotting import plot_detail
from uxps.model import Model, get_data_in_range

path = 'multiplex.txt'
mplx_dict = read_multiplex(path)
name = 'C 1s'
c1s = mplx_dict['C 1s']
plot_detail(c1s, name)
plt.show()

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
x, y = get_data_in_range(c1s['x'], c1s['y'], 275, 295)
colors = ['yellow', 'red']

model = Model(peaknames, mus, vary_mus, x_shift, vary_x_shift, sigmas, scales,
              ks, alpha, a0, a1, x, y)
model.fit()
model.plot_refinement(colors, name, 'dummy', True)
x_shift = model.pars['x_shift']
