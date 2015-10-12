#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
plot.py
-------

'''

from __future__ import print_function
from utils import ShowHelp, GetConf, GetOutput
import matplotlib.pyplot as pl
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.colors import ColorConverter
import argparse
import numpy as np; np.seterr(divide = 'ignore')

def AlphaMap(r = 0, g = 0, b = 0):
  '''
  
  '''
  cdict = {
            'red':  ((0.0, r, r),
                     (1.0, r, r)),

            'green': ((0.0, g, g),
                     (1.0, g, g)),

            'blue':  ((0.0, b, b),
                     (1.0, b, b)),
             
            'alpha': ((0.0, 0.1, 0.1),
                     (1.0, 1.0, 1.0))
          }
    
  return LinearSegmentedColormap('AlphaMap', cdict)

def SimplePlot(conf, output, xaxis, yaxis, alpha = None):
  '''

  '''
  
  # Names of all available params
  param_names = list(set([param.name for body in output.bodies for param in body.params]))
  
  # The x-axis parameter
  x = param_names[np.argmax(np.array([name.lower().startswith(xaxis.lower()) for name in param_names]))]  
  if not x.lower().startswith(xaxis.lower()):
    raise Exception('Parameter not understood: %s.' % xaxis)

  # The array of y-axis parameters
  if len(yaxis) == 0:
    # User didn't specify any; let's plot all of them
    yarr = list(set(param_names) - set([x]))
  else:
    yarr = []
    for yn in yaxis:
      y = param_names[np.argmax(np.array([name.lower().startswith(yn.lower()) for name in param_names]))]  
      if not y.lower().startswith(yn.lower()):
        raise Exception('Parameter not understood: %s.' % yn)
      yarr.append(y)

  # The alpha parameter
  if alpha is not None:
    a = param_names[np.argmax(np.array([name.lower().startswith(alpha.lower()) for name in param_names]))]  
    if not a.lower().startswith(alpha.lower()):
      raise Exception('Parameter not understood: %s.' % alpha)

  # We will only plot up to a maximum of ``conf.maxplots``  
  if len(yarr) > conf.maxplots:
    yarr = yarr[:conf.maxplots]

  # Set up the plot
  fig, ax = pl.subplots(len(yarr), 1, figsize = (conf.figwidth, (0.5 + len(yarr)) * conf.figheight))
  if not hasattr(ax, '__len__'):
    ax = [ax]
  if conf.tight_layout:
    fig.subplots_adjust(hspace = 0.1) 
  else:
    fig.subplots_adjust(hspace = 0.25)
  
  # Loop over all parameters (one subplot per each)
  for i, y in enumerate(yarr):
  
    # Axes limits
    ymin = np.inf
    ymax = -np.inf
    xmin = np.inf
    xmax = -np.inf
  
    # Loop over all bodies
    for b, body in enumerate(output.bodies):
    
      # Get indices of the parameters
      xi = np.where(x == np.array([param.name for param in body.params]))[0]
      yi = np.where(y == np.array([param.name for param in body.params]))[0]
      if alpha is not None:
        ai = np.where(a == np.array([param.name for param in body.params]))[0]
      else:
        ai = []
        
      # Are both x and y arrays preset for this body?
      if len(xi) and len(yi):
        xi = xi[0]
        yi = yi[0]
      else:
        continue
      
      if len(ai):
        ai = ai[0]
      else:
        ai = None
      
      # Get the arrays
      xpts = body.params[xi].array
      ypts = body.params[yi].array
              
      # Decide whether to plot individual legends
      if conf.legend_all:
        label = body.name
      else:
        label = None
      
      # Should we plot the first point if x = 0?
      if xpts[0] == 0. and conf.xlog and conf.skip_xzero_log:  
        xpts = xpts[1:]
        ypts = ypts[1:] 
      
      # Plot the curve
      if ai is None:
      
        # A simple solid color line
        ax[i].plot(xpts, ypts, conf.line_styles[b], label = label, lw = conf.linewidth)
      else:
                
        # Let's get fancy: make the curve opacity proportional to the `alpha` parameter
        apts = body.params[ai].array
        
        # Make logarithmic if necessary
        if conf.alog: 
          if apts[0] == 0.:
            apts = apts[1:]
          apts = np.log10(apts)
        
        points = np.array([xpts, ypts]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        lc = LineCollection(segments, cmap=AlphaMap(*ColorConverter().to_rgb(conf.line_styles[b][0])),
                            norm=pl.Normalize(np.nanmin(apts), np.nanmax(apts)))
        lc.set_array(apts)
        lc.set_linestyle(conf.line_styles[b][1:])
        lc.set_linewidth(conf.linewidth)
        lc.set_label(label)
        ax[i].add_collection(lc)
      
      # Limits
      if np.nanmin(xpts) < xmin:
        xmin = np.nanmin(xpts)
      if np.nanmin(ypts) < ymin:
        ymin = np.nanmin(ypts)
      if np.nanmax(xpts) > xmax:
        xmax = np.nanmax(xpts)
      if np.nanmax(ypts) > ymax:
        ymax = np.nanmax(ypts)
      
      # Labels
      ax[i].set_xlabel(body.params[xi].label(conf.short_labels), fontsize = conf.xlabel_fontsize)
      ax[i].set_ylabel(body.params[yi].label(conf.short_labels, conf.maxylabelsize), fontsize = conf.ylabel_fontsize)      
      
      # Tick sizes
      for tick in ax[i].xaxis.get_major_ticks():
        tick.label.set_fontsize(conf.xticklabel_fontsize) 
      for tick in ax[i].yaxis.get_major_ticks():
        tick.label.set_fontsize(conf.yticklabel_fontsize)
    
    # Log scale?
    if conf.xlog:
      if np.log(xmax) - np.log(xmin) > conf.xlog:
        if xmin > 0:
          ax[i].set_xscale('log')
    if conf.ylog:
      if np.log(ymax) - np.log(ymin) > conf.ylog:
        if ymin > 0:
          ax[i].set_yscale('log')
    
    # Tighten things up a bit
    if i < len(yarr) - 1:
      if conf.tight_layout:
        ax[i].set_xticklabels([])
      ax[i].set_xlabel('')
  
    # Add y-axis margins (doesn't work well with log)
    ax[i].margins(0., conf.ymargin)
  
    # Add a legend
    if conf.legend_all:
      ax[i].legend(loc = conf.legend_loc, fontsize = conf.legend_fontsize)
    elif i == 0:
      xlim = ax[i].get_xlim()
      ylim = ax[i].get_ylim()
      for b, body in enumerate(output.bodies):
        # HACK: Plot a line of length zero in the center of the plot so that it will show up on the legend
        foo = ax[i].plot([(xlim[0] + xlim[1])/2.],[(ylim[0] + ylim[1])/2.], conf.line_styles[b], label = body.name)
      ax[i].legend(loc = conf.legend_loc, fontsize = conf.legend_fontsize)
  
  # Add title
  if conf.title:
    if len(yarr) == 1:
      pl.title('VPLANET: %s' % output.sysname, fontsize = 24)
    else:
      pl.suptitle('VPLANET: %s' % output.sysname, fontsize = 24)

  return fig
  
if __name__ == '__main__':
  parser = argparse.ArgumentParser(prog = 'VPLOT', add_help = False)
  parser.add_argument("-h", "--help", nargs = '?', default = False, const = 1, help = 'Display the help')
  parser.add_argument("-b", "--bodies", nargs = '*', default = [], help = 'Bodies to plot; should match names of .in files')
  parser.add_argument("-x", "--xaxis", default = 'Time', help = 'Parameter to plot on the x-axis')
  parser.add_argument("-y", "--yaxis", nargs = '*', default = [], help = 'Parameter(s) to plot on the y-axis')
  parser.add_argument("-a", "--alpha", default = None, help = 'Parameter to control line alpha')
  args = parser.parse_args()

  # Help?
  if args.help:
    if args.help == 1:
      ShowHelp()
    else:
      ShowHelp(args.help)
    quit()

  # Initialize
  output = GetOutput(args.bodies)
  conf = GetConf()
  
  # Plot
  fig = SimplePlot(conf, output, args.xaxis, args.yaxis, args.alpha)

  # Show or save?
  if conf.interactive:
    pl.show()
  else:
    fig.savefig(conf.figname, bbox_inches = 'tight')