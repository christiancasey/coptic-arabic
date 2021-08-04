# -*- coding: utf-8 -*-


import csv
import re
import Levenshtein
import pyperclip
import numpy as np
import pickle

from collections import Counter


def copticSort(s):
    return re.sub( r'([ϣ-ϯϢ-Ϯ])', r'ⲱ\1', s.replace('ȣ', 'ⲩȣ') )
    

def excelCopy(m):
    s = '\n'.join([ '\t'.join(['%f' % mIJ for mIJ in mI]) for mI in m ])
    # pyperclip.copy(s)
    return s

vCoptic = []
vArabic = []

with open('parallel_texts.csv', newline='\n') as csvfile:
    reader = csv.DictReader(csvfile)    
    for row in reader:
        # Coptic-Arabic,Arabic,English,Error,Vocalized

        if row['Error']:
            continue

        sArabic = row['Arabic'].strip()
        sVocalized = row['Vocalized'].strip()
        sVocalized = sVocalized.replace('ْ', '')
        
        if sVocalized:
            sArabic = sVocalized
        else:
            continue
        
        if sArabic[-1] in [chr(i) for i in range(int('064b',16),int('0660',16))]:
            sArabic = sArabic[:-1]
        
        sArabic = 'ª' + sArabic + 'º'
        vArabic.append(sArabic)
        
        


        sCoptic = row['Coptic-Arabic'].strip()
        sCoptic = 'ª' + sCoptic + 'º'
        sCoptic = sCoptic.replace("'",'') # Get rid of the tick marks for now
        vCoptic.append(sCoptic)

nWords = len(vCoptic)

vCopticLetters = list(set(''.join(vCoptic)))
vCopticLetters = sorted(vCopticLetters, key=lambda s: copticSort(s))
vArabicLetters = sorted(list(set(''.join(vArabic))))
nCopticLetters = len(vCopticLetters)
nArabicLetters = len(vArabicLetters)


























if True:
    
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
    
if True:
        
    vLetterPairs = []
    for i in range(nWords):
        for cCoptic in vCoptic[i]:
            for cArabic in vArabic[i]:
                vLetterPairs.append([cCoptic, cArabic])

    # Sort the list of letter pairs for both scripts
    for i in range(2):
        vLetterPairs = sorted(vLetterPairs, key=lambda v: v[1-i])



    mOccurences = np.zeros([nCopticLetters, nArabicLetters])
    vCopticTotals = np.zeros([nCopticLetters, 1])
    vArabicTotals = np.zeros([1, nArabicLetters])
    iTotal = len(vLetterPairs)

    cCoptic = ''
    cArabic = ''
    for vPair in vLetterPairs:
        # if cCoptic == '•' or cArabic == '•':
        #     continue
        
        if not vPair[0] == cCoptic:
            cCoptic = vPair[0]
            iCoptic = vCopticLetters.index(cCoptic)

        if not vPair[1] == cArabic:
            cArabic = vPair[1]
            iArabic = vArabicLetters.index(cArabic)

        mOccurences[iCoptic,iArabic] += 1
        vCopticTotals[iCoptic,0] += 1
        vArabicTotals[0,iArabic] += 1

    # np.savetxt('output/Co-occurences (word level).csv', mOccurences, delimiter=',')


    mPhi = np.zeros([nCopticLetters, nArabicLetters])
    for i in range(nCopticLetters):
        for j in range(nArabicLetters):
            a = mOccurences[i,j]
            b = vArabicTotals[0,j] - a
            c = vCopticTotals[i,0] - a
            d = iTotal - b - c + a
            
            iNum = ( a*d - b*c )
            iDem = ( ( (a+b)*(c+d)*(a+c)*(b+d) ) ** 0.5 )
            iDem = iDem if iDem else 0.01
            mPhi[i,j] = iNum / iDem

    mPhi /= np.max(abs(mPhi))

    # np.savetxt('output/ⲫ (before alignment).csv', mPhi, delimiter=',')

    s = ''
    s += '\t'.join(vArabicLetters) + '\n'
    s += '\n'.join([ '\t'.join(['%f' % (phi*10) for phi in mPhiI]) for mPhiI in mPhi ])
    # s += '\n' + '\n'.join(vCopticLetters)

    # pyperclip.copy(s)



    sAlignments = ''
    for iAlignIter in range(10):
        
        
        print('\n'*10)
        print('Iteration %i' % (iAlignIter+1))
        print('\n'*10)
        
        # Alignment #############################################################################
        
        sAlignments += '\t'*40 + 'Iteration %i\n\n' % (iAlignIter+1) 
        vAlignments = []
        kWord = 10
        # for iWord in range(kWord,kWord+1):
        for iWord in range(nWords):
            sCoptic = vCoptic[iWord]
            sArabic = vArabic[iWord]
            n = len(sCoptic)
            m = len(sArabic)

            mScores = np.zeros([n,m])
            mAlign = np.zeros([n+1,m+1])
            for i in range(n):
                iCoptic = vCopticLetters.index(sCoptic[i])
                for j in range(m):
                    iArabic = vArabicLetters.index(sArabic[j])
                    mScores[i,j] = mPhi[iCoptic,iArabic]

            mAlign = np.zeros([n+1,m+1])
            mArrow = np.zeros([n+1,m+1])
            mArrow[:,0] = 2
            mArrow[0,0] = 1
            for i in range(1,n+1):
                for j in range(1,m+1):
                    fScale = 0.5

                    # Subtract the indel scores from their diagonal
                    # One should be well correlated and the other not
                    vDirections = [ mAlign[i,j-1] - mAlign[i-1,j], mAlign[i-1,j-1], mAlign[i-1,j] - mAlign[i,j-1] ]
                    vDirections = [ fScale * mAlign[i,j-1], mAlign[i-1,j-1], fScale * mAlign[i-1,j] ]
                    # vDirections = [ mAlign[i,j-1], mAlign[i-1,j-1], mAlign[i-1,j] ]
                    iMax = np.argmax(vDirections)

                    # Default to the diagonal
                    if (iMax == 0 and vDirections[0] <= vDirections[1]) or (iMax == 2 and vDirections[2] <= vDirections[1]):
                        iMax = 1

                    fMax = vDirections[iMax]

                    mAlign[i,j] = fMax + mScores[i-1,j-1]
                    mArrow[i,j] = iMax

            i = n
            j = m
            vAlignment = []
            while (i>0) and (j>0):

                vAlignment.insert(0,[i-1,j-1])

                iArrow = mArrow[i,j]
                i -= (iArrow>0)
                j -= (iArrow<2)

            vAlignments.append(vAlignment)
            v = ['←', '⬉', '↑']
     
            s = '\n' + '\t'*15 + 'Word #' + str(iWord+1) + '\n\n'

            s += '\t' + '\t'.join(sArabic) + '\n'
            s += '\n'.join([  sCoptic[i] + '\t' + '\t'.join(['%f' % mIJ for mIJ in mI]) for i, mI in enumerate(mScores) ])
            s += '\n'
            # s += excelCopy(mAlign)
            s += '\n'*2
            # '\n'.join([ '\t'.join(['%f' % mIJ for mIJ in mI]) for mI in m ])
            s += '\t'*1 + '\t'.join(sArabic) + '\n'
            s += '\n'.join([ '\t'*0 + sCoptic[i] + '\t' + '\t'.join([v[int(j)] for j in mI ]) for i, mI in enumerate(mArrow[1:,1:])])
            # s += '\n' + excelCopy(vAlignment)
            # pyperclip.copy(s)
            
            if (iWord+1 == 7):
                sAlignments += s + '\n\n'
                pyperclip.copy(sAlignments)


        
        # Recalculate co-occurences with newly aligned words

        mOccurences = np.zeros([nCopticLetters, nArabicLetters])
        vCopticTotals = np.zeros([nCopticLetters, 1])
        vArabicTotals = np.zeros([1, nArabicLetters])
        iTotal = 0

        for iWord in range(nWords):
            sCoptic = vCoptic[iWord]
            sArabic = vArabic[iWord]
            vAlignment = vAlignments[iWord]
            
            for vPair in vAlignment:
                iCoptic = vCopticLetters.index(sCoptic[vPair[0]])
                iArabic = vArabicLetters.index(sArabic[vPair[1]])
                
                mOccurences[iCoptic,iArabic] += 1
                vCopticTotals[iCoptic,0] += 1
                vArabicTotals[0,iArabic] += 1
                iTotal += 1



        mPhi = np.zeros([nCopticLetters, nArabicLetters])
        for i in range(nCopticLetters):
            for j in range(nArabicLetters):
                a = mOccurences[i,j]
                b = vArabicTotals[0,j] - a
                c = vCopticTotals[i,0] - a
                d = iTotal - b - c + a
                
                mPhi[i,j] = ( a*d - b*c ) / ( ( (a+b)*(c+d)*(a+c)*(b+d) ) ** 0.5 )

        mPhi /= np.max(abs(mPhi))


        # s = ''
        # s += '\t'.join(vArabicLetters) + '\n'
        # s += '\n'.join([ '\t'.join(['%f' % (phi) for phi in mPhiI]) for mPhiI in mPhi ])
        # pyperclip.copy(s)






    # print(sAlignments)
    pyperclip.copy(sAlignments)
    
    np.savetxt('output/Co-occurences (after alignment #' + str(iAlignIter) + '.csv', mOccurences, delimiter=',')
    np.savetxt('output/ⲫ (after alignment #' + str(iAlignIter) + '.csv', mPhi, delimiter=',')






    dAlignedTexts = { 'Coptic': vCoptic, 'Arabic': vArabic, 'Alignments': vAlignments }
    pickle.dump( dAlignedTexts, open( 'output/aligned_texts.p', 'wb' ) )



       
       