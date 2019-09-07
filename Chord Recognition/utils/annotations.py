import pandas as pd
import re

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
