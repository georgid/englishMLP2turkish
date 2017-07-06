
Scipt that prepares data for training GMMs mapping between phonemes of two different languages:
1) divides data into folds and concatenates the audio for all time-intervals for a given phoneme (according annotations)  into a wav file
Then processes all
2) extracts the features (phonetic posteriograms) 

not tested extensively

Tested From English phoneme models as feed forward network multilayer perceptron (MLP) onto a GMM Turkish phoneme models

Citation
--------------------

(G. Dzhambazov, 2017) Knowledge-based Probabilistic Modeling for Tracking Lyrics in Music Audio Signals
Chapter 3.4.2.2 and figure 3.7

Follows the idea of posteriogram mappings described as a fusion classifier in:
A. Kruspe - keyword spotting in acappela singing, ISMIR 2014



Usage 
------------------------
`extractFeatures.py` 

   	Next step: how to train the GMM models: see 
   	https://github.com/georgid/AlignmentDuration/blob/noteOnsets/src/hmm/continuous/MLP_fuzzyMappedHMM.py#L41

Depends on
--------------------
https://github.com/georgid/AlignmentDuration
and
www.cs.cmu.edu/~ymiao/pdnntk.html
