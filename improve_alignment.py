# -*- coding: utf-8 -*-


import csv
import re
import Levenshtein
import pyperclip
import numpy as np
import pickle


def copticSort(s):
    return re.sub( r'([ϣ-ϯϢ-Ϯ])', r'ⲱ\1', s.replace('ȣ', 'ⲩȣ') )


dAlignedTexts = pickle.load( open( 'output/aligned_texts.p', 'rb' ) )


vCoptic = dAlignedTexts['Coptic']
vArabic = dAlignedTexts['Arabic']
vAlignments = dAlignedTexts['Alignments']

nWords = len(vCoptic)

vCopticLetters = list(set(''.join(vCoptic)))
vCopticLetters = sorted(vCopticLetters, key=lambda s: copticSort(s))
vArabicLetters = sorted(list(set(''.join(vArabic))))
nCopticLetters = len(vCopticLetters)
nArabicLetters = len(vArabicLetters)


sAlignments = ''

kWord = 10
# for iWord in range(kWord,kWord+10):
for iWord in range(nWords):
    sCoptic = vCoptic[iWord]
    sArabic = vArabic[iWord]
    vCopticArabic = [ vCoptic[iWord], vArabic[iWord] ]
    vAlignment = np.transpose(np.array(vAlignments[iWord]))
    
    sAlignment = ''
    
    vAlignmentDisp = []
    for i in range(2):
        vWord = [ vCopticArabic[i][idx] for idx in vAlignment[i] ]
        # for j in range(vAlignment.shape[1]):
        #     # if j > 0 and vAlignment[i][j-1] == vAlignment[i][j]:
        #     #     vWord[j] = '(' + vWord[j] + ')'
        
        vAlignmentDisp.append( [str(x) for x in vAlignment[i]] )
        vAlignmentDisp.append( vWord )
    
    sAlignment = ''
    for i in [1, 0, 2, 3]:
        sAlignment += '\t'.join(vAlignmentDisp[i]) + '\n'
    
    sAlignments += '%i\n%s\n' % (iWord+1, sAlignment)

print(sAlignments)



pyperclip.copy(sAlignments)



mOccurences = np.zeros([nCopticLetters, nArabicLetters])
vCopticTotals = np.zeros([nCopticLetters, 1])
vArabicTotals = np.zeros([1, nArabicLetters])
iTotal = 0




















