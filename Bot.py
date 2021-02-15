import discord
import requests
import json
import os
import pathlib
import asyncio
from discord.ext import commands, tasks
from discord.ext.commands import CommandNotFound
pathlib.Path(__file__).parent.absolute()
filePath = pathlib.Path(__file__).absolute() #Current file's path
dirPath = pathlib.Path().absolute() #Current parent's path
realPath = dirPath/r'Discord/Krypts Assistant'
client = commands.Bot(command_prefix = ',', case_insensitive=True) #Prefix
print(r'◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼')
print(r'File        Path: ', filePath)
print(r'Directory   Path: ', dirPath)
print(r'- - - - - - - - - - - - - - - - - - - - - - - - - -')

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('something!'))
    print(r'''Started.''')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send('Command not recognised!')
        return
    raise error

@client.command(brief='')
async def info(ctx):
    await ctx.send('MineKrypt\'s Assistant | Prefix: , | Made for DisRoom™')

@client.command(brief='Displays the invite code.', aliases=('invite', 'i'))
async def inv(ctx):
    await ctx.send('Join DisRoom™! | discord.gg/7tJq6xH')

@client.command(aliases=('latency', 'p'))
async def ping(ctx):
    await ctx.send(f'Latency: *{round(client.latency * 1000)}ms*')

@client.command()
async def echo(ctx, echoed):
    # outchannel = client.get_channel(channelid)
    # await outchannel.send(echoed)
    await ctx.send(echoed)

# @client.command()
# @client.is_owner()
# async def close(ctx):
#     await ctx.send('Closing now! Please allow a few seconds.')
#     await client.close()

#^ FUCKING FUCK YOU RETARDED ASS API JSON BITCH GET THE FUCK OUT OF MY CODE
@client.command(aliases=('coronavirus', 'c19', 'covid'), brief='Depracated.')
async def covid19(ctx, *, country='totals'):
    url = f'https://covid-19-data.p.rapidapi.com/{country}'
    headers = {
        'x-rapidapi-key': '3950f2e5dcmsh92ecc9237a24cc1p1b99cajsn2f9a713cf54b',
        'x-rapidapi-host': 'covid-19-data.p.rapidapi.com'
        }
    response = requests.request('GET', url, headers=headers)
#    cases = {"confirmed":,"critical":,"deaths":,"recovered":}
    print(response.text.confirmed)
#    print(cases["critical"], sep=' | ')



client.run('NzIxOTgxOTQzMzY4OTA4ODEw.XuccFQ.exVUTT9Lz7VwZYmmE_TROLnrP80')