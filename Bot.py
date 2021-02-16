import discord
import requests
import json
import os
import pathlib
import asyncio
from googlesearch import search
from discord.ext import commands, tasks
from discord.ext.commands import CommandNotFound
from discord.ext.commands.cooldowns import BucketType
pathlib.Path(__file__).parent.absolute()
filePath = pathlib.Path(__file__).absolute() #Current file's path
dirPath = pathlib.Path().absolute() #Current parent's path
realPath = dirPath/r'Discord/Krypts Assistant'
client = commands.Bot(command_prefix = ',', case_insensitive=True) #Prefix
print(r'◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼')
print(r'File        Path: ', filePath)
print(r'Directory   Path: ', dirPath)
print(r'- - - - - - - - - - - - - - - - - - - - - - - - - -')
def is_owner(ctx):
    return ctx.message.author.id == 440068179994083328

#! Events

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name='MineKrypt die inside'))
    print(r'Started.')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send('Command not recognised!')
        return
    raise error

#! Commands

@client.command(aliases=('shutdown', 'stop', 'close'), hidden=True, description='Kills instance.')
@commands.check(is_owner)
async def kill(ctx):
    print('Shutting down...')
    await ctx.send('Stopped!')
    await client.close()

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
    await ctx.send(echoed)

@client.command()
async def echos(ctx, echoed):
    await ctx.message.delete()
    await ctx.send(echoed)

@client.command()
@commands.cooldown(1, 5)
async def userinfo(ctx, member: discord.Member):
    roles = [role for role in member.roles]
 
    embed = discord.Embed(colour = member.color, timestamp=ctx.message.created_at)
 
    embed.set_author(name=f"User Info - {member}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
 
    embed.add_field(name="ID:", value=member.id)
    embed.add_field(name="Guild name:", value=member.display_name)
    embed.add_field(name="Created at:", value=member.created_at.strftime("%a, %#d %B, %Y, %I:%M %p UTC"))
    embed.add_field(name="Joined at:", value=member.joined_at.strftime("%a, %#d %B, %Y, %I:%M %p UTC"))
    embed.add_field(name=f"Roles ({len(roles)})", value=" ".join([role.mention for role in roles]))
    embed.add_field(name="Top role:", value=member.top_role.mention)
    embed.add_field(name="Bot?", value=member.bot)
 
    await ctx.send(embed=embed)

    @userinfo.error
    async def userinfo_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'This command is on cooldown, but you can use it again in {round(error.retry_after, 2)} seconds!')

@client.command()
@commands.cooldown(1, 5)
async def serverinfo(ctx):
    name = str(ctx.guild.name)

    owner = str(ctx.guild.owner)
    id = str(ctx.guild.id)
    region = str(ctx.guild.region)
    memberCount = str(ctx.guild.member_count)

    icon = str(ctx.guild.icon_url)
    
    embed = discord.Embed(
        title=name + " Server Information",
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Server ID", value=id, inline=True)
    embed.add_field(name="Region", value=region, inline=True)
    embed.add_field(name="Member Count", value=memberCount, inline=True)

    await ctx.send(embed=embed)

    @serverinfo.error
    async def serverinfo_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'This command is on cooldown, but you can use it again in {round(error.retry_after, 2)} seconds!')

@client.command(aliases=('search', 'google'))
@commands.cooldown(1, 20)
async def find(ctx,*, query):
    author = ctx.author.mention
    await ctx.channel.send(f"Here are the links related to your question {author} !") 
    async with ctx.typing():
        for j in search(query, tld="com", num=3, stop=3, pause=2):
            await ctx.send(f"\n:point_right: {j}")
    @find.error
    async def find_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'This command is on cooldown, but you can use it again in {round(error.retry_after, 2)} seconds!')




@client.command()
@commands.cooldown(1, 20)
@commands.check(is_owner)
async def setgame(ctx, *, game='null'):
    await client.change_presence(status=discord.Status.online, activity=discord.Game(f'{game}'))
    await ctx.send(f'My game activity is now: {game}')
    print(f'My game activity is now: {game}')

    @setgame.error
    async def setgame_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'This command is on cooldown, but you can use it again in {round(error.retry_after, 2)} seconds!')

# @client.command()
# @client.is_owner()
# async def close(ctx):
#     await ctx.send('Closing now! Please allow a few seconds.')
#     await client.close()

# @client.command(aliases=('coronavirus', 'c19', 'covid'), brief='Depracated.')
# async def covid19(ctx, *, country='totals'):
#     url = f'https://covid-19-data.p.rapidapi.com/{country}'
#     headers = {
#         'x-rapidapi-key': '3950f2e5dcmsh92ecc9237a24cc1p1b99cajsn2f9a713cf54b',
#         'x-rapidapi-host': 'covid-19-data.p.rapidapi.com'
#         }
#     response = requests.request('GET', url, headers=headers)
# #    cases = {"confirmed":,"critical":,"deaths":,"recovered":}
#     print(response.text)
#     parsed = (json.loads(response))
#     print(json.dumps(parsed, indent=5, sort_keys=False))
# #    print(cases["critical"], sep=' | ')


#! To prepare files for push: $ git commit -am " "
#! To push files (This automatically runs the bot as well): $ git push heroku master
#! To view logs/console: $ heroku logs
#! To only run: $ heroku run Bot.py

client.run('NzIxOTgxOTQzMzY4OTA4ODEw.XuccFQ.exVUTT9Lz7VwZYmmE_TROLnrP80')