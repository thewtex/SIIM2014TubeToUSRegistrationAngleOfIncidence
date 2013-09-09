output_dir = './Data/Output/MonteCarlo'

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import os
import collections
import glob
from scipy import stats

mpl.rcdefaults()
mpl.rcParams['axes.labelsize'] = 'x-large'
mpl.rcParams['xtick.labelsize'] = 'large'
mpl.rcParams['ytick.labelsize'] = 'large'
mpl.rcParams['legend.fontsize'] = 'x-large'
mpl.rcParams['figure.dpi'] = 90

analyses = glob.glob(os.path.join(output_dir,'*Iterations = 8*'))
analyses = [os.path.basename(ii) for ii in analyses]
analyses.sort()
print(analyses)
angle_results = collections.OrderedDict()
translation_results = collections.OrderedDict()
for analysis in analyses:
    results = np.load(os.path.join(output_dir, analysis))
    angle_results[analysis[:-4]] = results['AngleError']
    translation_results[analysis[:-4]] = results['TranslationError']

fig = plt.figure(1)
ax = fig.add_subplot(121)
labels = angle_results.keys()
labels = ['$\\' + ii.split(',')[0] + '$' for ii in labels]
n_bins = 20
angle_range = (0.0, 0.01)
percent, bins, patches = ax.hist(angle_results.values(),
        bins=n_bins,
        range=angle_range,
        label=labels)
ax.legend()

print('\n\nangle error:')
for analysis, errors in angle_results.iteritems():
    print('\n' + analysis + ':')
    print('mean: ' + str(np.mean(errors)))
    print('std: ' + str(np.std(errors)))

print('\n\nT-test: (T-statistic, p-value)')
print(stats.ttest_ind(angle_results.values()[0], angle_results.values()[1]))

ax = fig.add_subplot(122)
labels = translation_results.keys()
labels = ['$\\' + ii.split(',')[0] + '$' for ii in labels]
translation_range = (0.0, 0.50)
percent, bins, patches = ax.hist(translation_results.values(),
        bins=n_bins,
        range=translation_range,
        label=labels)
ax.legend()

print('\n\ntranslation error:')
for analysis, errors in translation_results.iteritems():
    print('\n' + analysis + ':')
    print('mean: ' + str(np.mean(errors)))
    print('std: ' + str(np.std(errors)))

print('\n\nT-test: (T-statistic, p-value)')
print(stats.ttest_ind(translation_results.values()[0], translation_results.values()[1]))
#plt.show()
