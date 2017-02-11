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
PHONEMELIST = ['AA']


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

def segment_phonemes(whichFold):
    annoFiles = []
    for i,f in enumerate(AUDIO_REC_IDS):
        f_URI_name=   f + '/' + f + '.TextGrid'
        if whichFold == i:
            print 'leaving the one out: ' +  f_URI_name
            continue
        annoFiles.append(f_URI_name)
    
    
    for annoFile in annoFiles:
        audioSeg = [np.empty([0,0], dtype='int16')] * len(PHONEMELIST)
    
        audioFile = annoFile.replace('.TextGrid', '.wav')
        fs, audio = scipy.io.wavfile.read(os.path.join(audioPath, audioFile))
        # get 1 channel
        if np.shape(audio)[-1] == 2:
            audio = audio[:, 0]
    
        print audioFile, fs, audio. shape
    
        tgfile = tgt.read_textgrid(os.path.join(annoPath,annoFile))
        tgfile.get_tier_names()
        tier_details = tgfile.get_tier_by_name("phonemes")
        
        for phoneme in tier_details:
            try:
                idx = PHONEMELIST.index(phoneme.text)
            except ValueError:
                continue
    
            start = int(float(phoneme._get_start_time()) * fs)
            end = int(float(phoneme._get_end_time()) * fs)
            audioSeg[idx] = np.append(audioSeg[idx], audio[start : end])
        
        for i in range(len(PHONEMELIST)):
            # segDir = os.path.join('../data/phonemeSeg/', PHONEMELIST[i] + '.wav')
            # segDir = os.path.join('../data/phonemeSeg/', PHONEMELIST_RENAME[i] + '.wav')
            segDir = os.path.join(segPath, PHONEMELIST[i] + '.wav')
            if os.path.exists(segDir):
                fs, audioOld = scipy.io.wavfile.read(segDir)
                audioNew = np.append(audioOld, audioSeg[i])
                scipy.io.wavfile.write(segDir, fs, audioNew)
            else:
                scipy.io.wavfile.write(segDir, fs, audioSeg[i])
