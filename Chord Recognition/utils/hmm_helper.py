import pandas as pd
import numpy as np
import os

from utils.annotations import read_simplify_chord_file

COL_NAMES_NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

def __calc_prob_chord(chord_group):
    chord_group_count = chord_group.groupby('sequence_chord').size().reset_index()
    chord_group_count.columns = ['sequence_chord', 'count']
    total = chord_group_count['count'].sum()
    chord_group_count['transition_prob'] = chord_group_count['count']/total
    return chord_group_count

def calc_transition_prob_matrix(chords_annotation, test_version=False):
    initial_chords = chords_annotation['chord'].values[:-1]
    sequence_chord = chords_annotation['chord'][1:].tolist()

    sequence_chords = pd.DataFrame({'initial_chords': initial_chords, 'sequence_chord': sequence_chord})
    prob_matrix = sequence_chords.groupby('initial_chords').apply(__calc_prob_chord).reset_index().drop('level_1', axis=1)
    prob_matrix = prob_matrix.pivot(index='initial_chords', columns='sequence_chord', values='transition_prob')
    prob_matrix.append(pd.Series(np.zeros(prob_matrix.shape[1]), name='<END>'))
    prob_matrix = prob_matrix.fillna(0)
    if(test_version == False):
        prob_matrix['<START>'] = 0.
        prob_matrix.loc['<END>'] = 0.
        prob_matrix.loc['<END>', '<END>'] = 1
    return prob_matrix

def __get_mu_array(note_feature_vector):
    return note_feature_vector[COL_NAMES_NOTES].mean()

def get_mu_sigma_from_chroma(chromagram):
    mu_array = chromagram.groupby('chord').apply(__get_mu_array)

    states_cov_matrices = []
    for name, group in chromagram.groupby('chord'): # alphabetic order
        states_cov_matrices.append(group[COL_NAMES_NOTES].cov().values)
    states_cov_matrices = np.array(states_cov_matrices)

    return [mu_array, states_cov_matrices]

def create_ISPM(transition_matrix):
    transition_matrix_cols = list(transition_matrix.index.values)

    initial_states_prob = pd.Series(np.zeros(len(transition_matrix_cols)), index=transition_matrix_cols)
    initial_states_prob[0] = 1
    return initial_states_prob.sort_index()

def get_hmm_predictions(chord_ix_predictions, ix_2_chord):
    return np.array([ix_2_chord[chord_ix] for chord_ix in chord_ix_predictions])


def calc_initial_state_prob_matrix(process_silence=False, annotations_folder_path='lab_and_musics'):
    first_chords = []
    for file_str in os.listdir(annotations_folder_path):
        if(file_str.endswith('.lab')):
            chords_annotation_ = read_simplify_chord_file(f'{annotations_folder_path}/{file_str}', process_silence)
            first_chords.append(chords_annotation_['chord'].values[0])

    first_chord_counts = np.unique(first_chords, return_counts=True)
    initial_state_probs = pd.Series(first_chord_counts[1]/first_chord_counts[1].sum(), index=first_chord_counts[0])
    return initial_state_probs

def adapt_initial_prob_matrix(init_states, transition_matrix):
    filtered_initial_states = init_states[transition_matrix.columns.values]
    filtered_initial_states = filtered_initial_states/filtered_initial_states.sum()
    return filtered_initial_states.fillna(0)
