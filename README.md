
Makes fuzzy mapping between phonemes of two different languages.
Done, but ont restricted to: From English phoneme models as feed forward network multilayer perceptron network onto a GMM turksih phoneme models

Follows the idea of posteriogram mappings described as a fusion classifier in:
A. Kruspe - keyword spotting in acappela singing, ISMIR 2014

Usage 
------------------------
`extractFeatures`

extract the audio segments from many audio files and concatentate it in a wav file
    then one can extract features from that audio (see etractFeatures script)

   	how to train the GMM models: see 
   	https://github.com/georgid/AlignmentDuration/blob/noteOnsets/src/hmm/continuous/MLP_fuzzyMappedHMM.py#L41
