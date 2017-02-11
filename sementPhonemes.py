# -*- coding: utf-8 -*-
# modified from  https://github.com/elitrout/lyrics/blob/b1c74e11f6392f384b3b8533ad7ef8a3c9917b10/code/segmentPhonemeMTG.py

import scipy.io.wavfile
import numpy as np
import os.path
from os import listdir
from os.path import isfile, join

import tgt


PHONEMELIST = ['AA' ,'E', 'IY', 'I', 'O', 'U', 'OE', 'UE', 'B', 'D', 'GG', 'H', 'KK', 'LL', 'M', 'NN', 'P', 'RR', 'S', 'SH',\
 'T',  'Y', 'Z', 'C', 'CH', 'F', 'J', 'sil']
PHONEMELIST = ['AA'] # do  for only one phoneme


AUDIO_REC_IDS = [
'2ec806b4-7df2-4fd4-9752-140a0bcc9730',
'f5a89c06-d9bc-4425-a8e6-0f44f7c108ef',
'feda89e3-a50d-4ff8-87d4-c1e531cc1233',
'b49c633c-5059-4658-a6e0-9f84a1ffb08b',
# '727cff89-392f-4d15-926d-63b2697d7f3f'
# '567b6a3c-0f08-42f8-b844-e9affdc9d215'
### 4 folds without last two
]

#### use leave-one out
num_folds = len(AUDIO_REC_IDS)

whichFold = 0
audioPath = '/Users/joro/Documents/ISTANBULSymbTr2/'
segPath = audioPath + '/phonemeAudio/' + str(num_folds) + 'folds/fold' + str(whichFold + 1)
annoPath = audioPath 


def write_audio_to_file( audioSeg):
    '''
    write the audioSeg for each phoneme to file
    Parameters
    ----------------------
    audioSeg: list(nd.arrray)
        audio chunks with concatenated audio for each phoneme
    
    '''
    
    for i in range(len(PHONEMELIST)): # segDir = os.path.join('../data/phonemeSeg/', PHONEMELIST[i] + '.wav')
        # segDir = os.path.join('../data/phonemeSeg/', PHONEMELIST_RENAME[i] + '.wav')
        segDir = os.path.join(segPath, PHONEMELIST[i] + '.wav')
        
        if os.path.exists(segDir): # read the existing audio from previous phonemes, concatenate new audio and store
            fs, audioOld = scipy.io.wavfile.read(segDir)
            audioNew = np.append(audioOld, audioSeg[i])
            scipy.io.wavfile.write(segDir, fs, audioNew)
        else: 
            scipy.io.wavfile.write(segDir, fs, audioSeg[i]) # write new audio

def concat_phoneme_audio(tier_phonemes, curr_file_audio, all_audio_seg, fs):
    '''
    concatenate audio for each phoneme from tier_phonemes
    modifies all_audio_seg
    
    Parameters
    ------------------------
    
    curr_file_audio: nd.array
        complete audio for file  
    
    all_audio_seg: list(nd.array)
        audio chunks with concatenated audio for each phoneme
        
    '''
    for phoneme in tier_phonemes: # for each phoneme
        try:
            idx = PHONEMELIST.index(phoneme.text)
        except ValueError:
            continue

        start = int(float(phoneme._get_start_time()) * fs)
        end = int(float(phoneme._get_end_time()) * fs)
        all_audio_seg[idx] = np.append(all_audio_seg[idx], curr_file_audio[start : end]) # concatenate the corresponding segment
        
        return all_audio_seg


def get_list_anno_files(AUDIO_REC_IDS, whichFold):
    '''
     exclude one annotation file for leave-one-out cross validation

    '''
    annoFiles = []
    for i,f in enumerate(AUDIO_REC_IDS):
        f_URI_name=   f + '/' + f + '.TextGrid'
        if whichFold == i:
            print 'leaving the one out: ' +  f_URI_name
            continue
        annoFiles.append(f_URI_name)
    return annoFiles   
        
def segment_phonemes(whichFold):
    '''

    for each phoneme: extract the audio segments from many audio files and concatentate it in a wav file
    then one can extract features from that audio (see etractFeatures script)
    
    all_audio_seg:  the concatenated audio
    '''
     
    annoFiles = get_list_anno_files (AUDIO_REC_IDS, whichFold)
    
    
    for annoFile in annoFiles: # loop in all annotation files
        all_audio_seg = [np.empty([0,0], dtype='int16')] * len(PHONEMELIST) # chunks of concatenated curr_file_audio for each phonemes
    
        audioFile = annoFile.replace('.TextGrid', '.wav')
        fs, curr_file_audio = scipy.io.wavfile.read(os.path.join(audioPath, audioFile))
        # get 1 channel
        if np.shape(curr_file_audio)[-1] == 2:
            curr_file_audio = curr_file_audio[:, 0]
    
        print audioFile, fs, curr_file_audio. shape
        
        ######### read phoneme annotations
        tgfile = tgt.read_textgrid(os.path.join(annoPath,annoFile))
        tgfile.get_tier_names()
        tier_phonemes = tgfile.get_tier_by_name("phonemes")
        
        
        all_audio_seg = concat_phoneme_audio(tier_phonemes, curr_file_audio, all_audio_seg, fs)
        
        ## write the all_audio_seg for each phoneme to file
        write_audio_to_file(all_audio_seg)
