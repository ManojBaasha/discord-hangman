#! usr/bin/python3
import discord
import os
import random
from discord.ext import commands

client = discord.Client()

client=commands.Bot(command_prefix='m.')
'''setting a prefix for the bot'''

with open('token.txt') as f:
    """ using a text file to store the discord bot token"""
    token = f.read()
    
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

#######################################################################

@client.command()
async def hangman(ctx, *, Mode=None): 
    '''using m.hangman as the command to run the game'''
    global WORDLIST_FILENAME
    global secretWord
    if Mode == None:
        await ctx.send("Welcome to HangMan!! ")
        await ctx.send("select a topic \n Movies \n Games \n Animals \n Use m.hangman <topic>")
        return

    if Mode == "Movies":
        WORDLIST_FILENAME = "movies.txt"

    if Mode == "Games":
        WORDLIST_FILENAME = "games.txt"

    if Mode == "Animals":
        WORDLIST_FILENAME = "animals.txt"

    

    def loadwords():
        inFile = open(WORDLIST_FILENAME, 'r')
        line = inFile.readline()

        wordlist = line.split()
        secretWord = random.choice(wordlist)
        return secretWord

    secretWord = loadwords()
    global mistakeMade
    global lettersGuessed
    print(secretWord)
    mistakeMade=0
    lettersGuessed=[]
    
    
@client.command()
async def guess(ctx, *, word=None):
    global secretWord
    global mistakeMade
    if word == None:
        await ctx.send("Enter a letter to guess")
        return

    if word == "Start":
        await ctx.send("I am thinking of a word that is ")
        await ctx.send( len(secretWord))
        await ctx.send( " letters long \n Use m.guess <letter> to guess the letters of the word, START")
        return

    def isWordGuessed(secretWord, lettersGuessed):
        c=0
        for i in lettersGuessed:
            if i in secretWord:
                c+=1
        if c==len(secretWord):
            return True
        else:
            return False

    def getGuessedWord(secretWord, lettersGuessed):
        s=[]
        for i in secretWord:
            if i in lettersGuessed:
                s.append(i)
        ans=''
        for i in secretWord:
            if i in s:
                ans+=i
            else:
                ans+='_'
        return ans

    def getAvailableLetters(lettersGuessed):

        import string
        ans=list(string.ascii_lowercase)
        for i in lettersGuessed:
            ans.remove(i)
        return ''.join(ans)

    
    global lettersGuessed
    

    while 10 - mistakeMade >0:
        
        if isWordGuessed(secretWord,lettersGuessed):
            await ctx.send("_____________")
            await ctx.send("YOU WON YOU BIG BRAIN")
            break
        

        else:
            guess= word
            if guess in lettersGuessed:
                await ctx.send("Yo U already Guessed that letter smh")
                await ctx.send(getGuessedWord(secretWord,lettersGuessed))

            elif guess in secretWord and guess not in lettersGuessed:
                lettersGuessed.append(guess)
                await ctx.send("wow lucky guess, u got it right")
                await ctx.send(getGuessedWord(secretWord,lettersGuessed))

            else:
                lettersGuessed.append(guess)
                mistakeMade +=1
                await ctx.send("HaHa that aint the letter")
                await ctx.send(getGuessedWord(secretWord,lettersGuessed))

        

        await ctx.send("U Have")
        await ctx.send(10-mistakeMade)
        await ctx.send("guesses left")
        break 

        

        
        if 8-mistakeMade == 0:
            await ctx.send("Youve ran out of guesses you small brain hehe :p")
            break

        


#######################################################################

    
client.run(token)
