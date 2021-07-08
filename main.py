#! usr/bin/python3
import discord
import os


client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

with open('token.txt') as f:
    """ using a text file to store the discord bot token"""
    token = f.read()
        
client.run(token)
