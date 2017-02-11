'''
Created on Nov 30, 2016

@author: joro
'''
import os
import subprocess
import logging
import sys
import htkmfc
import numpy
import pickle
from sementPhonemes import PHONEMELIST, segPath
from sklearn import mixture
from numpy import mean, cov
path_to_hcopy = ''

FeatureExtractor_URI = '/Users/joro/Documents/Phd/UPF/voxforge/myScripts/AlignmentDuration/'
if FeatureExtractor_URI not in sys.path:
    sys.path.append(FeatureExtractor_URI)
    
from src.align.FeatureExtractor import FeatureExtractor

path_pdnn = '/Users/joro/Downloads/pdnn/'
if path_pdnn not in sys.path:
        sys.path.append(path_pdnn)
import cmds.run_Extract_Feats

def extract_MFCC(audio_URI, output_URI):

        fe = FeatureExtractor('/usr/local/bin/HCopy', None)
        # call htk to extract features
        URImfcFile = fe._extractMFCCs( audio_URI)

        # read features form binary htk file
        logging.debug("reading MFCCs from {} ...".format(URImfcFile))
        HTKFeat_reader =  htkmfc.open(URImfcFile, 'rb')
        mfccsFeatrues = HTKFeat_reader.getall()
        
        labels = numpy.zeros( len(mfccsFeatrues), dtype = 'float32')
        
        
        with open(output_URI,'w') as f:
            pickle.dump((mfccsFeatrues,labels),f)
        return output_URI

      


if __name__ == '__main__':
    ##@## run only once
#     segment_phonemes(whichFold)

    
    for phoneme in PHONEMELIST:
        audio_one_phoneme_URI = os.path.join(segPath, phoneme + '.wav')
        phoneme_mfcc_URI_ = audio_one_phoneme_URI[:-4] + '.mfccs.pkl'
        if not os.path.exists(phoneme_mfcc_URI_):
            phoneme_mfcc_URI_ = extract_MFCC(audio_one_phoneme_URI)
        cmds.run_Extract_Feats.main(['--data', phoneme_mfcc_URI_, '--nnet-param', '/Users/joro/Downloads/dampB.mdl', '--nnet_cfg', '/Users/joro/Downloads/dampB.cfg', \
                  '--output_file', audio_one_phoneme_URI[:-4] + '.PPG',   'layer_index',  -1,  '--batch_size', 100    ])
