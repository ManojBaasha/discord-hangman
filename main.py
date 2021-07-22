#! usr/bin/python3
import discord
import os
import random
from discord.ext import commands

#####################################################################
"""the basic commands to run the bot on discord"""

client = discord.Client()

client=commands.Bot(command_prefix='m.')#setting a prefix for the bot.In this case "m." is the prefix

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
        await ctx.send("select a topic \n    Movies \n    Games \n    Animals \n Use m.hangman <topic>")
        return

    if Mode == "Movies":
        WORDLIST_FILENAME = "movies.txt"

    if Mode == "Games":
        WORDLIST_FILENAME = "games.txt"

    if Mode == "Animals":
        WORDLIST_FILENAME = "animals.txt"

    

    def loadwords():#this function allots a secret word from the text file chosen by the user
        inFile = open(WORDLIST_FILENAME, 'r')
        line = inFile.readline()

        wordlist = line.split()
        secretWord = random.choice(wordlist)
        return secretWord

    secretWord = loadwords()
    global mistakeMade
    global lettersGuessed
    print(secretWord)
    """making variables global to use it in other functions as well"""
    mistakeMade=0
    lettersGuessed=[]

    await ctx.send("I am thinking of a word that is "+ str(len(secretWord)) + " letters long \n Use m.guess <letter> to guess the letters of the word")
    
    
@client.command()
async def guess(ctx, *, word=None):
    global secretWord
    global mistakeMade
    if word == None:
        await ctx.send("Enter a letter to guess")
        return

    def isWordGuessed(secretWord, lettersGuessed):#this funtion is called when the user guesses the correct letter
        c=0
        for i in lettersGuessed:
            if i in secretWord:
                c+=1
        if c==len(secretWord):
            return True
        else:
            return False

    def getGuessedWord(secretWord, lettersGuessed):#forms the overall word based on the users letters guesses and the missing letters
        s=[]
        for i in secretWord:
            if i in lettersGuessed:
                s.append(i)
        ans=''
        for i in secretWord:
            if i in s:
                ans+=i
            else:
                ans+='\_ '
        return ans

    
    global lettersGuessed

    
    while 10 - mistakeMade >0:
        guess= word
        if guess in lettersGuessed:
            await ctx.send("You already guessed that letter, try again")
            await ctx.send(getGuessedWord(secretWord,lettersGuessed))

        if guess in secretWord and guess not in lettersGuessed:
            lettersGuessed.append(guess)
            await ctx.send("wow lucky guess, u got it right")
            await ctx.send(getGuessedWord(secretWord,lettersGuessed))

        if guess not in secretWord and guess not in lettersGuessed:
            lettersGuessed.append(guess)
            mistakeMade +=1
            await ctx.send("wrong letter , choose again")
            await ctx.send(getGuessedWord(secretWord,lettersGuessed))

        if isWordGuessed(secretWord,lettersGuessed):
            await ctx.send("\~\~\~\~\~\~")
            await ctx.send("YOU WON!!!!!!!")
            break

        await ctx.send("U Have " + str(10-mistakeMade) + " guesses left" )

        if 10-mistakeMade == 0:
            await ctx.send("Youve ran out of guesses,gg ")
            await ctx.send("the word was " + str(secretWord))
            break
        break
        


#######################################################################

    
client.run(token)
