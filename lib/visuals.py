import matplotlib.pyplot as plt
import numpy as np

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