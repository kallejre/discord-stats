#!/usr/bin/python
# -*- coding: utf-8 -*-
import random

def mad_stuff(fname='estonian-words.txt'):  # Tähestiku statistika.
    f=''.join(sorted(open(fname).read().lower())).strip()
    for i in sorted(set(f)): print(i, f.count(i))
def let2regi(letter):
    if letter=='_':
        return '||:stop_button:||'
    if letter in "abcdefghijklmnopqrstuvwxyz":
        return ':regional_indicator_'+letter+':'
    return letter
class hangman():
    def __init__(self,diff=None):
        self.cheats= 0  # Annab juurde 16 lisakatset ja näitab, mis tähed on sõnas.
        self.alphabet = " !'-abcdefghijklmnopqrstuvwxyzäéõöüšž"
        self.alp2="` !'-äéõöüšž` või `a-z` (kaasa arvatud tühik)"
        self.letter_storage = []
        # Osa, mis sõltub sõna valimisest.
        if not diff:
            diff=3
        if diff==1:
            fname = 'hang_estonian-words.txt'
            self.wordList=list(filter(lambda x:4<len(x)<=8, map(lambda x:x.strip(),open(fname).readlines())))
        if diff==2:
            fname = 'hang_estonian-words.txt'
            self.wordList=list(filter(lambda x:8<len(x)<=12, map(lambda x:x.strip(),open(fname).readlines())))
        if diff==3:
            fname = 'hang_estonian-words2.txt'
            self.wordList=list(filter(lambda x:len(x)<=16, map(lambda x:x.strip(),open(fname).readlines())))
        if diff==4:
            fname = 'hang_estonian-words2.txt'
            self.wordList=list(filter(lambda x:16<len(x)<=20, map(lambda x:x.strip(),open(fname).readlines())))
        if diff==5:
            fname = 'hang_estonian-words2.txt'
            self.wordList=list(filter(lambda x:20<len(x), map(lambda x:x.strip(),open(fname).readlines())))
        self.secretWord = random.choice(self.wordList)  # lets randomize single word from the list
        self.wlen = len(self.secretWord)
        self.guess_word = ['_'] * self.wlen

        
        self.guess_taken = 1
        self.max_guess=10+16*int(self.cheats)
        if self.cheats:
            print(''.join(sorted(set(self.secretWord),key=lambda x:self.secretWord.count(x))))
        self.startup='Otsitava sõna pikkus on '+str(self.wlen)+' tähte.\nVõimalikud tähed saavad olla '+self.alp2
    @property
    def type(self):
        return 'Hangman `'+''.join(self.guess_word)+'`'
    def guess(self, guess):
        guess = guess.lower()
        output = []
        gameOver=False
        if not (guess in self.alphabet or guess in self.secretWord):  # checking input
            output.append('Täht peab olema vahemikust '+self.alp2)
        elif guess in self.letter_storage:
            output.append('Seda on juba proovitud!')
        else:
            self.letter_storage.append(guess)
            if guess in self.secretWord:
                output.append('Õige!')
                if len(guess)==1:
                    for x in range(0, self.wlen):
                        if self.secretWord[x] == guess:
                            self.guess_word[x] = guess
                else:
                    for x in range(0, self.wlen-len(guess)+1):  # töödeldud
                        if self.secretWord[x:x+len(guess)] == guess:
                            for y in range(x,x+len(guess)):
                                self.guess_word[y] = guess[y-x]

                if not '_' in self.guess_word:
                    gameOver=True
                    output.append('Mäng läbi :grinning:\nVastus oli '+self.secretWord)
                    return '\n'.join(output), gameOver
            else:
                output.append('Vale!')
                if self.guess_taken == self.max_guess:
                    gameOver=True
                    output.append('Mäng läbi! :frowning2:\nVastus oli '+self.secretWord)
                self.guess_taken += 1
        
        output.append('Proovitud: '+' '.join(sorted(self.letter_storage))+'\nSõna: **'+
              ''.join(list(map(let2regi,self.guess_word)))+ '**\nValesti proovitud: '+ str(self.guess_taken-1) + '/'+ str(self.max_guess) + 'korda.')
        return '  '.join(output), gameOver
"""     
game=hangman()
print(game.guess('a'))
print(game.guess('e'))
print(game.guess('i'))
print(game.guess('o'))
print(game.guess('k'))
print(game.guess('s'))
"""
