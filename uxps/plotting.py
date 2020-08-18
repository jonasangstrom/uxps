import matplotlib.pyplot as plt


def plot_refinement(x_obs, y_obs, y_calc, back, peaks, colors, labels, lower,
                    upper, title, residual, folder, show_plots):
    plt.title(title)
    plt.scatter(x_obs,  y_obs, color='red', label='$y_{obs}$')
    plt.plot(x_obs, y_calc, color='black', label='$y_{calc}$')
    plt.plot(x_obs, back, '--', color='black', label='$background$')
    plt.plot(x_obs, residual, color='blue', label='$y_{calc}-y_{obs}$')
    for label, peak, color in zip(labels, peaks, colors):
        plt.fill_between(x_obs, peak+back, back, label=label, color=color,
                         alpha=0.5)
    plt.xlim(upper, lower)
    plt.xlabel('E/eV')
    plt.legend()
    if show_plots:
        plt.show()
    else:
        plt.savefig(folder+'\\'+title.split(',')[0]+'.png', dpi=500)
        plt.close('all')


def plot_detail(detail, name, scale=1, offset=0, s=1):
    x_raw, y = detail['x'], detail['y']
    x = x_raw - offset
    plt.scatter(x, y/scale, label=name, s=1)
    plt.xlim(x.max(), x.min())
    plt.xlabel('E/eV')
    plt.title(name)
    plt.show()


def plot_all_multiplex(mplx_dict, colors, models_dict=None, offset=3,
                       show_plots=True, s=1, folder=''):
    ''' Plots mplx_dict or model if avaliable (not implemented)
    '''
    for name in mplx_dict:
        if models_dict is not None:
            if name in models_dict:
                models_dict[name].plot_refinement(colors, name, folder,
                                                  show_plots)
            else:
                plot_detail(mplx_dict[name], name, offset, s)
        else:
            plot_detail(mplx_dict[name], name, offset, s)
