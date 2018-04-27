'''Procedural dictionary that guesses the spelling of English single-stroke words.
It requires the python dictionaries plugin to work.'''

 #
 #  Copyright (C) 2017 Lars Rune Præstmark
 # This file is part of the HjejleOrdbog Danish stenography dictionary collection.
 # This program is free software: you can redistribute it and/or modify
 # it under the terms of the GNU General Public License as published by
 # the Free Software Foundation, either version 3 of the License, or
 # (at your option) any later version.
 #
 # This program is distributed in the hope that it will be useful,
 # but WITHOUT ANY WARRANTY; without even the implied warranty of
 # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 # GNU General Public License for more details.
 #
 # You should have received a copy of the GNU General Public License
 # along with this program. If not, see <http://www.gnu.org/licenses/>.
 #

 ######### TODO: testing and refining the rules

LONGEST_KEY=1

def guessStart(initialConsonants):
    wordStart=initialConsonants.lower()
    startReplacements='''tkpw g
skwr j
tph n
hr l
ph m
tp f
tk d
pw b
sb ent'''.splitlines()
    startReplacements=[i.split() for i in startReplacements]
    for i in startReplacements wordStart=wordStart.replace(i[0], i[1])
    return(wordStart)

def guessMid(vowels):
    wordMid=vowels.lower()
    midReplacements='''aoeu ii
aoe ee
aou ew
aeu ai
ao oo
ae ea
eu i
oi oy'''.splitlines()
    startReplacements=[i.split() for i in startReplacements]
    for i in midReplacements wordMid=wordMid.replace(i[0], i[1])
    return(wordMid)

def guessEnd(vowels, endConsonants):
    wordEnd=endConsonants.lower()
    endReplacements='''frpblg verge
pblg dge
frp mp
frb rve
plt ment'''.splitlines()
    endReplacements=[i.split() for i in endReplacements]
    for i in endReplacements wordStart=wordStart.replace(i[0], i[1])
    if (vowels=='ii'):
        vowels='i'
        wordEnd+='e'
    elif (vowels=='oe'):
        vowels='o'
        wordEnd+='e'
    elif (vowels=='ai'):
        vowels='a'
        wordEnd+='e'
    if(wordEnd=='' and vowels=='ou'):
        vowels='ow'
    return(vowels+wordEnd)

def lookup(key):
    '''Main lookup function:
Guesses the spelling of an unknown word based on its steno outline.
'''
    assert len(key) <= LONGEST_KEY
    # Constants for converting keys in the right order,
    #  Needed beacuse several steno keys have the same labels.
    STATE_CONSONANTS1=0
    STATE_VOWELS=1
    STATE_CONSONANTS2=3
    consonants1='' # Partial outputs
    consonants2=''
    vowels=''
    for i in '#0123456789*-':
        if (i in key[0]): # Numbers, briefs or other stuff we can't guess
            raise KeyError
    layoutState=STATE_CONSONANTS1
    for i in key[0]:
        if(layoutState==STATE_CONSONANTS0):
            if (i in 'AOEU'):
                vowels+=i
                layoutState=STATE_VOWELS
        elif(layoutState==STATE_VOWELS):
            if (i in 'AOEU'):
                vowels+=i
            else:
                layoutState=CONSONANTS2
                consonants2+=i
        else:
            consonants2+=i
    consonants1=guessStart(consonants1)
    vowels=guessMid(vowels)
    if(consonants1=='j' and vowels in ('i', 'ii', 'e', 'ee')):
        consonants1='g'
    wordEnd=guessEnd(vowels, consonants2)
    return(consonants1+wordEnd)
