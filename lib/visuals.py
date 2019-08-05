import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec
from matplotlib.ticker import AutoMinorLocator
import scipy.stats    
import matplotlib.lines as mlines       

def plotPdf(interval, values, rng, xlim=None):

    #### Colocar cor diferente nas áreas abaixo do gráfico

    fig, ax = plt.subplots()
    ax.plot(interval, values, 'k')
    
    if not np.isscalar(rng) and len(rng)==1:
        rng = rng[0]
    
    if not np.isscalar(rng):
        x_1 = np.argmax(interval>rng[0])
        x_2 = np.argmax(interval>rng[1])
        ax.fill_between(np.linspace(rng[0], rng[1], num=len(values[x_1:x_2])), values[x_1:x_2], color='k')
    else:
        x = np.argmax(interval>rng)
        x_0 = interval[0]
        ax.fill_between(np.linspace(x_0, rng, num=len(values[0:x])), values[0:x], color='k')
        
    ax.axhline(0, c='k', alpha=.5)
    ax.axvline(0, c='k', alpha=.5)
         
    ax.yaxis.grid(b=True, which='minor', color='k', linestyle='--', alpha=.2, zorder=0) 
    ax.yaxis.grid(b=True, which='major', color='k', linestyle='--', alpha=.5, zorder=0) 

    ax.set_facecolor('xkcd:white')
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    
    if xlim != None:
         ax.set_xlim(xlim)



def prettifyAx(ax, spinesToRemove):
    ax.set_facecolor('xkcd:white')
    for spine in spinesToRemove:
        ax.spines[spine].set_visible(False)
    

def jointplot(df, kind_main='scatter'):
    df_columns = df.columns
    
    x = df[df_columns[0]].values
    y = df[df_columns[1]].values
    
    fig = plt.figure(figsize=(8,8))
    gs = gridspec.GridSpec(3, 3)
    
    ax_main = plt.subplot(gs[1:3, 1:3])
    ax_xDist = plt.subplot(gs[0, 1:3], sharex=ax_main)
    ax_yDist = plt.subplot(gs[1:3, 0], sharey=ax_main)

    ### Main

    ax_main.xaxis.tick_top()
    
    if kind_main == 'scatter':
        main_color = '#071EA9'
        mean_x = np.mean(x)
        mean_y = np.mean(y)
        median_x = np.median(x)
        median_y = np.median(y)
        mean_color = 'y'
        median_color = 'r'
        
        ax_main.scatter(x, y, marker='.', zorder=0, c=main_color)
        
        ax_main.plot(mean_x, mean_y, 'yo', zorder=1)
        ax_main.plot(median_x, median_y, 'ro', zorder=1)       
        mean_marker = mlines.Line2D([], [], color=mean_color, marker='o', linestyle='None', label='Mean')
        median_marker = mlines.Line2D([], [], color=median_color, marker='o', linestyle='None', label='Median')
        ax_main.legend(handles=[mean_marker, median_marker], framealpha=.5)
        
        ax_main.set(xlabel=df_columns[0], ylabel=df_columns[1])    
        ax_main.yaxis.set_minor_locator(AutoMinorLocator(2))
        ax_main.xaxis.set_minor_locator(AutoMinorLocator(2))
        ax_main.grid(b=True, which='minor', color='k', linestyle='--', alpha=.2, zorder=1) 
        ax_main.grid(b=True, which='major', color='k', linestyle='--', alpha=.5, zorder=1) 

    else:
        nbins = 20
        colormap = plt.cm.GnBu
        k = scipy.stats.kde.gaussian_kde(df.values.T)
        xi, yi = np.mgrid[x.min():x.max():nbins*1j, y.min():y.max():nbins*1j]
        zi = k(np.vstack([xi.flatten(), yi.flatten()]))
        if kind_main == 'kde':
            ax_main.pcolormesh(xi, yi, zi.reshape(xi.shape), cmap=colormap)
        elif kind_main == 'hexbin':
            ax_main.hexbin(x, y, gridsize=nbins, cmap=colormap)
        elif kind_main == '2dhist':
            ax_main.hist2d(x, y, bins=nbins, cmap=colormap)
        elif kind_main == 'density':
            ax_main.pcolormesh(xi, yi, zi.reshape(xi.shape), cmap=colormap)
        elif kind_main == 'dens_shading':
            ax_main.pcolormesh(xi, yi, zi.reshape(xi.shape), shading='gouraud', cmap=colormap)
        elif kind_main == 'contour':
            ax_main.pcolormesh(xi, yi, zi.reshape(xi.shape), shading='gouraud', cmap=colormap)
            ax_main.contour(xi, yi, zi.reshape(xi.shape) )


    
    ### Dist. and Cumulative Dist.
    hist_color = '#071EA9'
    cumDist_color = '#3CBCC2'
    marginal_nBins = 40
    nBins = 30
    cum_nBins = 30
    
    # X    
    cnt, edges = np.histogram(x, bins=cum_nBins, density=True)
    
    ax_xDist.hist(x, bins=nBins, align='mid', color=hist_color, density=True)
    ax_xDist.set(ylabel='freq')
    hist_dist = scipy.stats.rv_histogram((cnt, edges))
    pdf = hist_dist.pdf(edges)

    n_mean = 2
    smoothed_pdf = np.zeros(pdf.size)
    for i in range(n_mean, smoothed_pdf.size - n_mean):
        smoothed_pdf[i] = np.mean(pdf[i-n_mean:i+n_mean])  
    ax_xDist.plot(edges, smoothed_pdf, c='r')    
    
    ax_xCumDist = ax_xDist.twinx()
    ax_xCumDist.plot(edges, hist_dist.cdf(edges))
    ax_xCumDist.tick_params('y')#, colors=cumDist_color)
    ax_xCumDist.set_ylabel('cumulative')#, color=cumDist_color)
    
    for ax in [ax_xDist, ax_xCumDist]:
        ax.tick_params(axis='x', which='both', top=False, bottom=False, labelbottom=False) 
        
    ax_xDist.xaxis.set_minor_locator(AutoMinorLocator(2))
    ax_xDist.grid(b=True, which='minor', color='k', linestyle='--', alpha=.2, zorder=1) 
    ax_xDist.grid(b=True, which='major', color='k', linestyle='--', alpha=.5, zorder=1)

    # Y    
    cnt, edges = np.histogram(y, bins=cum_nBins, density=True)
    
    ax_yDist.hist(y, bins=nBins, orientation='horizontal', align='mid', color=hist_color, density=True)
    ax_yDist.set(xlabel='freq')
    hist_dist = scipy.stats.rv_histogram((cnt, edges))
    pdf = hist_dist.pdf(edges)
    
    n_mean = 2
    smoothed_pdf = np.zeros(pdf.size)
    for i in range(n_mean, smoothed_pdf.size - n_mean):
        smoothed_pdf[i] = np.mean(pdf[i-n_mean:i+n_mean])  
    ax_yDist.plot(smoothed_pdf, edges, c='r')
    
    ax_yCumDist = ax_yDist.twiny()
    ax_yCumDist.plot(hist_dist.cdf(edges), edges, zorder=1, c=cumDist_color)
    ax_yCumDist.tick_params('x')#, colors=cumDist_color)
    ax_yCumDist.set_xlabel('cumulative')#, color=cumDist_color)
    
    for ax in [ax_yDist, ax_yCumDist]:
        ax.set_xlim(ax.get_xlim()[::-1])
        ax.tick_params(axis='y', which='both', right=False, left=False, labelleft=False)   
    
    ax_yDist.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax_yDist.grid(b=True, which='minor', color='k', linestyle='--', alpha=.2, zorder=1) 
    ax_yDist.grid(b=True, which='major', color='k', linestyle='--', alpha=.5, zorder=1)

    ### Prettify plots
    prettifyAx(ax_main, ['bottom', 'right'])
    prettifyAx(ax_xDist, ['top', 'bottom'])
    prettifyAx(ax_xCumDist, ['top', 'bottom'])
    prettifyAx(ax_yDist, ['left', 'right'])
    prettifyAx(ax_yCumDist, ['left', 'right'])

    plt.tight_layout()