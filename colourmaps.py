from matplotlib.cm import Purples, Blues, Greens, Oranges, Reds
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
from math import floor, ceil, modf

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

colourmaps = [Purples,
              Blues,
              Greens,
              Oranges,
              Reds,
              LinearSegmentedColormap('darkblue', darkblue_map),
              LinearSegmentedColormap('pinks', pinks_map),
              LinearSegmentedColormap('yellows', yellows_map),
              LinearSegmentedColormap('lightblue', lightblue_map),
              LinearSegmentedColormap('darkpink', darkpink_map)]

def get_colourmap(number: float):
    """Returns a vertically stacked array containing
    the amount of colourmaps specified by number
    """
    assert number <= SIZE
    result = [colourmaps[i](np.linspace(0., 1, 1000))
              for i in range(floor(number))]

    result.append(colourmaps[ceil(number) - 1](np.linspace(0., modf(number)[0], 
                                           floor(modf(number)[0] * 1000))))

    return np.vstack(result)
