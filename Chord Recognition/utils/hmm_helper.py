import pandas as pd

def __calc_prob_chord(chord_group):
    chord_group_count = chord_group.groupby('sequence_chord').size().reset_index()
    chord_group_count.columns = ['sequence_chord', 'count']
    total = chord_group_count['count'].sum()
    chord_group_count['transition_prob'] = chord_group_count['count']/total
    return chord_group_count

def calc_transition_prob_matrix(chords_annotation):
    initial_chords = chords_annotation['chord'].values[:-1]
    sequence_chord = chords_annotation['chord'][1:].tolist()

    sequence_chords = pd.DataFrame({'initial_chords': initial_chords, 'sequence_chord': sequence_chord})
    prob_matrix = sequence_chords.groupby('initial_chords').apply(__calc_prob_chord).reset_index().drop('level_1', axis=1)
    prob_matrix = prob_matrix.pivot(index='initial_chords', columns='sequence_chord', values='transition_prob')
    return prob_matrix.fillna(0)
