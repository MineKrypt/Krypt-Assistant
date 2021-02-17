import discord
import requests
import json
import os
import pathlib
from datetime import datetime
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

snipe_message_author = {}
snipe_message_content = {}

@client.event
async def on_message_delete(message):
     snipe_message_author[message.channel.id] = message.author
     snipe_message_content[message.channel.id] = message.content
     del snipe_message_author[message.channel.id]
     del snipe_message_content[message.channel.id]

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name='for commands'))
    print(r'Started.')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send('Command not recognised!')
        return
    raise error

#! Commands

@client.command(aliases=('stop', 'kill', 'close'))
@commands.check(is_owner)
async def shutdown(ctx):
    await ctx.send('Closing now...')
    await client.logout()

@client.command()
async def info(ctx):
    await ctx.send('| MineKrypt\'s Assistant | Prefix: , | Made for DisRoom™ | v1.6')

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
async def uptime(ctx):
    now = datetime.utcnow()
    elapsed = now - starttime
    seconds = elapsed.seconds
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    await ctx.send("Running for {}d {}h {}m {}s".format(elapsed.days, hours, minutes, seconds))

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
    await ctx.channel.send(f'Here are the links related to your question {author} ! *Query: "{query}"*')
    async with ctx.typing():
        for j in search(query, tld="com", num=3, stop=3, pause=2):
            await ctx.send(f"\n:zap: | {j}")

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

@client.command()
@commands.cooldown(1, 10)
async def snipe(ctx):
    channel = ctx.channel
    try: #This piece of code is run if the bot finds anything in the dictionary
        em = discord.Embed(name = f"Last deleted message in #{channel.name}", description = snipe_message_content[channel.id])
        em.set_footer(text = f"This message was sent by {snipe_message_author[channel.id]}")
        await ctx.send(embed = em)
    except: #This piece of code is run if the bot doesn't find anything in the dictionary
        await ctx.send(f"I couldn't find any recently deleted messages in #{channel.name} !")

    @snipe.error
    async def snipe_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'This command is on cooldown, but you can use it again in {round(error.retry_after, 2)} seconds!')

@client.command()
async def dm(ctx, member: discord.Member=None):
  if member == None:
    await ctx.send('Mention a member')
    return
  try:
    for a in range(5):
      await member.send("text")

  except commands.CommandInvokeError:
      await ctx.send("Couldn't send message to user")




#! To prepare files for push: $ git commit -am " "
#! To push files (This automatically runs the bot as well): $ git push heroku master
#! To view logs/console: $ heroku logs
#! To only run: $ heroku run Bot.py

starttime = datetime.utcnow()
client.run('NzIxOTgxOTQzMzY4OTA4ODEw.XuccFQ.exVUTT9Lz7VwZYmmE_TROLnrP80')