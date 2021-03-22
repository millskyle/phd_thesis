import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import subprocess
import os


def spineless(a):
    a.spines['right'].set_visible(False)
    a.spines['top'].set_visible(False)


def single_wide(height=3.5):
    fig, ax = plt.subplots(1,1,figsize=(37/6,height))
    return fig, [ax]
    
def double_wide(height=3, labels=["a)","b)"]):
    _ = plt.subplots(1,2,figsize=(37/6,height))
    for l,ax in zip(labels,_[1]):
        ax.text(0.05, 0.95, l, va='top', ha='left', transform=ax.transAxes )
    return _

def triple_wide(height=2.5, labels=["a)","b)","c)"]):
    _ = plt.subplots(1,3,figsize=(37/6,height))
    for l,ax in zip(labels,_[1]):
        ax.text(0.05, 0.95, l, va='top', ha='left', transform=ax.transAxes )
    return _

def six_plots(height=5.0, labels=["a)","b)","c)","d)","e)","f)"], flatten=True):
    _ = plt.subplots(2,3,figsize=(37/6,height))
    for l,ax in zip(labels,_[1].flatten()):
        ax.text(0.05, 0.95, l, va='top', ha='left', transform=ax.transAxes )
    return _[0], _[1].flatten()


plt.style.use('../kyle.mplstyle')

GRAYCOLOR=GREYCOLOR='#AA9999'
COLORS = plt.rcParams['axes.prop_cycle'].by_key()['color']

def publish_figure(name='figure.pdf', tex=False):
    import subprocess
    import os
    fname=f"figs/{name}"
    os.makedirs("./figs", exist_ok=True)
    fig = plt.gcf()
    fig.savefig(fname)
    subprocess.run(['git','add', fname], capture_output=True)
    subprocess.run(['git','commit','-m','updated'], capture_output=True)
    subprocess.run(['git','push','origin','main'], capture_output=True)
    print(f"https://github.com/millskyle/phd_thesis/raw/main/methods/{fname}")
    if tex:
        print("""
\begin{figure}[tb]
  \centering
  \includegraphics{graphics/methods/"""+name+"""}
  \caption{}
  \label{fig:"""+name.replace(".pdf","") + """}
\end{figure}
         """)
    

def draw_ann(ax, xy=(0,0), layers=[5,4,1], spacing=None, bounds=None, colors=None, text=None,
            text_offset=None, dropout=1.0, seed=1):
    np.random.seed(seed)
    if spacing is None:
        spacing = [2,]*(len(layers)-1)
    if colors is None:
        colors = [None,]*(len(layers))
    p = []
    layer_x = xy[0]
    layer_ys = [xy[1]-0.5*L for L in layers]

    for l,L in enumerate(layers):
        c = colors[l]
        if c is None:
            c = [plt.rcParams['axes.prop_cycle'].by_key()['color'][0]]*layers[l]
        else:
            assert len(c)==layers[l], "Length of specified colours must match the number of nodes in the layer"
        for i in range(layers[l]): #for each node
            p.append(matplotlib.patches.Circle((layer_x,layer_ys[l]+i), 0.4, color=c[i], zorder=100))
            if text is not None:
                if text[l] is not None:
                    if text[l][i] is not None:
                        try:
                            to = text_offset[l]
                            if to is None: to=[0,0]
                        except:
                            to=[0,0]
                            pass
                        ax.text(layer_x+to[0], layer_ys[l]+i+to[1], text[l][i], va='center', ha='center',color='white',zorder=101, )
            if l+1 < len(layers):
                if np.random.rand() < dropout:
                        params=dict(linestyle='-', zorder=10, color=c[i])
                else:
                        params=dict(linestyle='--', zorder=10, color=c[i], alpha=0.4)
                for j in range(layers[l+1]):
                    
                        
                    p.append(matplotlib.lines.Line2D((layer_x, layer_x+spacing[l]),(layer_ys[l]+i, layer_ys[l+1]+j), **params))
    
        if l+1 < len(layers):
            layer_x += spacing[l]

            
            
    if bounds is None:
        bounds = []
    else:
        bounds = [bounds]
        
    for a in p:
        ax.add_artist(a)
        
        if isinstance(a,matplotlib.lines.Line2D):
            b = a.get_path().get_extents()    
        else:
            b = a.get_extents()
        b = b.transformed(ax.transData.inverted())
        bounds.append([b.x0, b.x1, b.y0, b.y1])
    
    minn = np.min(bounds, axis=0)
    maxx = np.max(bounds, axis=0)
    
    bounds = [minn[0], maxx[1], minn[2], maxx[3] ]
    
    ax.set_xlim(bounds[0:2])
    ax.set_ylim(bounds[2:4])
    
    ax.set_aspect(1)
    return bounds