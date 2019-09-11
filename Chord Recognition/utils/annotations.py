import pandas as pd
import numpy as np
import re
import pretty_midi
import IPython # listen to sounds on Python
import librosa

def __simplify_chords(chords_df):
    chords_processed = chords_df['chord'].str.split(':maj')                         # remove major x chords return array of array
    chords_processed = [elem[0] for elem in chords_processed]                       # further process step above to return 1 array
    chords_processed = [elem.split('/')[0] for elem in chords_processed]            # remove inverted chords
    chords_processed = [elem.split('aug')[0] for elem in chords_processed]          # remove augmented chords
    chords_processed = [elem.split(':(')[0] for elem in chords_processed]           # remove added notes chords
    chords_processed = [elem.split('(')[0] for elem in chords_processed]            # remove added notes chords 2
    chords_processed = [elem.split(':sus')[0] for elem in chords_processed]         # remove sustained chords
    chords_processed = [re.split(":?\d", elem)[0] for elem in chords_processed]     # remove added note
    chords_processed = [elem.replace('dim', 'min') for elem in chords_processed]    # change diminute to minor
    chords_processed = [elem.replace('hmin', 'min') for elem in chords_processed]   # change semi-diminute to minor
    chords_processed = [re.split(":$", elem)[0] for elem in chords_processed]       # remove added notes chords
    return chords_processed

def read_simplify_chord_file(music_file_path, process_silence=False):
    chords_annotation = pd.read_csv(music_file_path, sep=" ", header=None)
    chords_annotation.columns = ['start', 'end', 'chord']
    chords_annotation['chord'] = __simplify_chords(chords_annotation)
    if(process_silence == True): # replace silence by probable tonal end
        chords_annotation.loc[chords_annotation['chord'] == 'N', 'chord'] = chords_annotation['chord'].mode()[0]
    return chords_annotation

def simplify_predicted_chords(chromagram, predicted_col='predicted'):
    change_chord = chromagram[predicted_col] != chromagram[predicted_col].shift(-1)
    change_chord_ix = change_chord[change_chord == True].index
    filtered_pcp = chromagram.loc[change_chord_ix].copy()
    end_time_previous = np.array([0] + filtered_pcp['end'][:-1].tolist())
    filtered_pcp['start'] = end_time_previous
    return filtered_pcp[['chord', predicted_col, 'start', 'end']].reset_index(drop=True)

def get_chord_notes(chord, chord_type='major'):
    notes = ['A','A#','B','C','C#','D','D#','E','F','F#','G','G#']
    ix_2_notes = {i:notes[i] for i in range(12)}
    notes_2_ix = {notes[i]:i for i in range(12)}

    major_steps = [4, 7]
    minor_steps = [3, 7]

    chord_ix_init = np.array(notes_2_ix[chord])
    if(chord_type=='major'):
        steps = chord_ix_init + major_steps
    else:
        steps = chord_ix_init + minor_steps

    array_steps = steps%12
    extra_chord_notes = [ix_2_notes[step] for step in array_steps]
    chord_list = [chord] + extra_chord_notes
    return chord_list

def create_simple_midi(chords_simplified, tempo, predicted_col='predicted'):
    notes_str = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
    # https://en.scratch-wiki.info/wiki/MIDI_Notes
    midi_pitch_note = list(np.arange(60,72)) # 60 to 71
    notes_2_midi = {note_str:midi_pitch for note_str, midi_pitch in zip(notes_str, midi_pitch_note)}

    pm = pretty_midi.PrettyMIDI(initial_tempo=tempo)
    inst1 = pretty_midi.Instrument(program=42, is_drum=False, name='note1')
    inst2 = pretty_midi.Instrument(program=42, is_drum=False, name='note2')
    inst3 = pretty_midi.Instrument(program=42, is_drum=False, name='note3')
    velocity = 1000
    TONIC = 12

    for ix, row in chords_simplified.iterrows():
        chord_start_time = row['start']
        chord_end_time = row['end']

        chord_type = 'major'
        # get chord notes
        if(len(row[predicted_col]) > 1): # name contains > than 1 letter = minor chord FOR NOW
            chord_type = 'minor'
        chord_notes = get_chord_notes(row[predicted_col].split(':')[0], chord_type)

        inst1.notes.append(pretty_midi.Note(velocity, notes_2_midi[chord_notes[0]] - TONIC, chord_start_time, chord_end_time))
        inst2.notes.append(pretty_midi.Note(velocity, notes_2_midi[chord_notes[1]], chord_start_time, chord_end_time))
        inst3.notes.append(pretty_midi.Note(velocity, notes_2_midi[chord_notes[2]], chord_start_time, chord_end_time))

    pm.instruments.append(inst1)
    pm.instruments.append(inst2)
    pm.instruments.append(inst3)

    fs = 16000
    return IPython.display.Audio(pm.synthesize(fs=16000), rate=16000)
