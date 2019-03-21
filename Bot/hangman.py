#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import sys

wordList = list(map(lambda x:x.strip(),open('hang_estonian-words.txt').readlines()))
wordList.sort(key=len)
wordList=wordList[-10:]
cheats=False
guess_word = []
secretWord = random.choice(wordList)  # lets randomize single word from the list
length_word = len(secretWord)
alphabet = " !'-abcdefghijklmnopqrstuvwxyzäéõöüšž"
letter_storage = []
if cheats:print(''.join(sorted(set(secretWord),key=lambda x:secretWord.count(x))))
def mad_stuff(fname='estonian-words.txt'):
    f=''.join(sorted(open(fname).read().lower())).strip()
    for i in sorted(set(f)):
        print(i, f.count(i))
#print(secretWord)

def change():
    for character in secretWord:  # printing blanks for each letter in secret word
        guess_word.append('_')

    print ('Ok, so the word You need to guess has', length_word,
           'characters')

    print( 'Be aware that You can enter only 1 letter from a-z\n\n')
    print(guess_word)
def guessing():
    guess_taken = 1
    max_guess=10+16*int(cheats)
    while guess_taken < max_guess:
        print(' '.join(sorted(letter_storage)))
        print(''.join(guess_word))
        print(guess_taken, '/',max_guess)
        guess = input('Pick a letter\n').lower()
        if not (guess in alphabet or guess in secretWord):  # checking input
            print('Enter a letter from a-z alphabet')
        elif guess in letter_storage:
            # checking if letter has been already used
            print('You have already guessed that letter!')
        else:
            letter_storage.append(guess)
            if guess in secretWord:
                print('You guessed correctly!')
                if len(guess)==1:
                    for x in range(0, length_word):
                        # This Part I just don't get it
                        if secretWord[x] == guess:
                            guess_word[x] = guess
                else:
                    for x in range(0, length_word-len(guess)+1):### töödeldud
                        if secretWord[x:x+len(guess)] == guess:
                            for y in range(x,x+len(guess)):
                                guess_word[y] = guess[y-x]
                print(''.join(guess_word))

                if not '_' in guess_word:
                    print('You won!')
                    break
            else:
                print('The letter is not in the word. Try Again!')
                guess_taken += 1
                if guess_taken == 10:
                    print (' Sorry Mate, You lost :<! The secret word was'
                           , secretWord)


change()
guessing()

print('Game Over!')
#mad_stuff()		
