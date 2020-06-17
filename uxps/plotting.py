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


def plot_detail(detail, name, offset=0):
    x_raw, y = detail['x'], detail['y']
    x = x_raw - offset
    plt.scatter(x, y)
    plt.xlim(x.max(), x.min())
    plt.xlabel('E/eV')
    plt.title(name)
    plt.tight_layout()
    plt.show()
