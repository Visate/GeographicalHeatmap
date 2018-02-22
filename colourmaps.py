from matplotlib.cm import Purples, Blues, Greens, Oranges, Reds
from matplotlib.colors import LinearSegmentedColormap
import numpy as np 

SIZE = 10

pinks_map = {'red': ((0, 1, 1),
                     (1, 1, 1)),

             'green': ((0, 0, 0),
                       (1, 0, 0)),
                   
             'blue': ((0, 1, 1),
                      (1, 1, 1)),
                 
             'alpha': ((0, 0, 0),
                       (1, 1, 1))}

yellows_map = {'red': ((0, 1, 1),
                       (1, 1, 1)),

               'green': ((0, 1, 1),
                         (1, 1, 1)),
                   
               'blue': ((0, 0, 0),
                        (1, 0, 0)),
                 
               'alpha': ((0, 0, 0),
                         (1, 1, 1))}

lightblue_map = {'red': ((0, 0, 0),
                         (1, 0, 0)),

                 'green': ((0, 1, 1),
                           (1, 1, 1)),
                   
                 'blue': ((0, 1, 1),
                          (1, 1, 1)),
                 
                 'alpha': ((0, 0, 0),
                           (1, 1, 1))}

darkpink_map = {'red': ((0, 0.7, 0.7),
                        (1, 0.7, 0.7)),

                'green': ((0, 0.22, 0.22),
                          (1, 0.22, 0.22)),
                   
                'blue': ((0, 0.45, 0.45),
                         (1, 0.45, 0.45)),
                 
                'alpha': ((0, 0, 0),
                          (1, 1, 1))}

darkblue_map = {'red': ((0, 0.04, 0.04),
                        (1, 0.04, 0.04)),

                'green': ((0, 0.18, 0.18),
                          (1, 0.18, 0.18)),
                   
                'blue': ((0, 0.4, 0.4),
                         (1, 0.4, 0.4)),
                 
                'alpha': ((0, 0, 0),
                          (1, 1, 1))}

colourmaps = [Purples(np.linspace(0., 1, 256)),
              Blues(np.linspace(0., 1, 256)),
              Greens(np.linspace(0., 1, 256)),
              Oranges(np.linspace(0., 1, 256)),
              Reds(np.linspace(0., 1, 256)),
              LinearSegmentedColormap('darkblue', darkblue_map)(np.linspace(0., 1, 256)),
              LinearSegmentedColormap('pinks', pinks_map)(np.linspace(0., 1, 256)),
              LinearSegmentedColormap('yellows', yellows_map)(np.linspace(0., 1, 256)),
              LinearSegmentedColormap('lightblue', lightblue_map)(np.linspace(0., 1, 256)),
              LinearSegmentedColormap('darkpink', darkpink_map)(np.linspace(0., 1, 256))]

def get_colourmap(number: int):
    """Returns a vertically stacked array containing
    the amount of colourmaps specified by number
    """
    if number > len(colourmaps):
        number = len(colourmaps)
    return np.vstack(colourmaps[:number])
