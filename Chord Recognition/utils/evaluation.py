import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from sklearn.metrics import f1_score
from itertools import product
from matplotlib import colors


def calc_classification_stats(chromagram):
    obs = np.transpose(pd.get_dummies(chromagram['chord']))
    pred = np.transpose(pd.get_dummies(chromagram['predicted']))

    true_positives = np.logical_and(obs, pred).astype(np.int)
    true_positives.index = [f'{elem}-TP' for elem in true_positives.index]

    false_positives = obs - pred
    false_positives = np.less(false_positives, 0).astype(int)
    false_positives = 2 * false_positives
    false_positives.index = [f'{elem}-FP' for elem in false_positives.index]

    false_negatives = obs - pred
    false_negatives = np.greater(false_negatives, 0).astype(int)
    false_negatives = 3 * false_negatives
    false_negatives.index = [f'{elem}-FN' for elem in false_negatives.index]

    f1_score_ = f1_score(chromagram['chord'], chromagram['predicted'], average='micro')

    return (true_positives, false_positives, false_negatives, f1_score_)

def plot_performance(true_positives, false_positives, false_negatives, frame_duration_sec):
    all_chords_list_maj = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    all_chords_list_min = [f'{elem}:min' for elem in all_chords_list_maj]
    all_chords_list = all_chords_list_min + all_chords_list_maj
    stats_str = ['-TP', '-FP', '-FN']

    key_combination = list(product(all_chords_list, stats_str))
    key_combination = [f'{e1}{e2}' for e1,e2 in key_combination]

    vis_matrix = pd.DataFrame(np.zeros([len(key_combination),true_positives.shape[1]]), index=key_combination)
    vis_matrix.loc[true_positives.index] = vis_matrix.loc[true_positives.index] + true_positives
    vis_matrix.loc[false_positives.index] = vis_matrix.loc[false_positives.index] + false_positives
    vis_matrix.loc[false_negatives.index] = vis_matrix.loc[false_negatives.index] + false_negatives

    plt.figure(figsize=[15,6])

    plt.yticks(np.arange(0,vis_matrix.shape[0],3), all_chords_list);
    # generate x-label times in seconds
    xlabel_locations = np.round(np.linspace(0,true_positives.shape[1]-1, 5)).astype(int)
    xlabel_ticks = pd.date_range('2019-01-01', periods=true_positives.shape[1], freq=f'{round(frame_duration_sec * 1000)}ms')
    xlabel_ticks = np.round(xlabel_ticks.second + (xlabel_ticks.microsecond/1000000), 2)
    plt.xticks(xlabel_locations, xlabel_ticks[xlabel_locations])

    plt.xlabel('Time(s)');
    plt.ylabel('Chords');

    plt.title('Chord Recognition Results')

    cmap = colors.ListedColormap(['white', 'green', 'red', 'black'])

    im = plt.imshow(vis_matrix, aspect='auto', cmap=cmap)

    # https://stackoverflow.com/questions/25482876/how-to-add-legend-to-imshow-in-matplotlib
    # get the colors of the values, according to the
    # colormap used by imshow
    values = np.unique(vis_matrix.values)
    colors_ = [im.cmap(im.norm(value)) for value in values]
    # create a patch (proxy artist) for every color
    legend_labels = {1:'True Positive', 2: 'False Positive', 3: 'False Negative'}
    patches = [mpatches.Patch(color=colors_[i], label=legend_labels[i]) for i in range(1,len(values)) ]
    # put those patched as legend-handles into the legend
    plt.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0. )
