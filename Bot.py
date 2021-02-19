import discord #Discord.py
import requests #Web requests
import json #Parse json
import os
import pathlib #Reach files
import psutil #OS info
import platform #OS info
from datetime import datetime
from googlesearch import search #Google search
from discord.ext import commands, tasks #Discord.py commands
from discord.ext.commands import CommandNotFound #Discord.py errors
from discord.ext.commands.cooldowns import BucketType #Discord.py cooldowns
pathlib.Path(__file__).parent.absolute()
filePath = pathlib.Path(__file__).absolute() #Current file's path
dirPath = pathlib.Path().absolute() #Current parent's path
realPath = dirPath/r'Discord/Krypts Assistant'
client = commands.Bot(command_prefix = ',', case_insensitive=True) #Prefix
print(r'◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼')
print(r'File        Path: ', filePath)
print(r'Directory   Path: ', dirPath)
print(r'- - - - - - - - - - - - - - - - - - - - - - - - - -')
def is_owner(ctx): #Discord user ID's granted admin permissions
    return ctx.message.author.id == 440068179994083328

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

#! Events

snipe_message_author = {}
snipe_message_content = {}

@client.event
async def on_message_delete(message): #Getting the messages for the snipe command
    snipe_message_author[message.channel.id] = message.author
    snipe_message_content[message.channel.id] = message.content

@client.event
async def on_ready(): #This will execute when the bot comes online
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name='for commands'))
    print(r'Started.')

@client.event
async def on_command_error(ctx, error): #Executes when a command
    if isinstance(error, CommandNotFound):
        await ctx.send('Command not recognised!')
        return
    raise error

#! Commands

@client.command()
@commands.cooldown(1, 5)
async def info(ctx): #This will show some information about the bot
    await ctx.send('| MineKrypt\'s Assistant | Prefix: , | Made for DisRoom™ | v1.10')

@client.command(brief='Displays the invite code.', aliases=('invite', 'i'))
@commands.cooldown(1, 30)
async def inv(ctx): #This will give an invite
    await ctx.send('Join DisRoom™! | discord.gg/7tJq6xH')

@client.command(aliases=('latency', 'p'))
@commands.cooldown(1, 5)
async def ping(ctx): #This will show the latency to discord
    await ctx.send(f'Latency: *{round(client.latency * 1000)}ms*')

@client.command(aliases=('say', 'rpt'))
@commands.cooldown(1, 5)
async def echo(ctx, echoed): #This will repeat text
    await ctx.send(echoed)

@client.command()
@commands.cooldown(1, 5)
async def echos(ctx, echoed): #This will repeat text and delete the original command
    await ctx.message.delete()
    await ctx.send(echoed)

@client.command()
@commands.cooldown(1, 5)
async def uptime(ctx): #This will show how long the bot has been online
    now = datetime.utcnow()
    elapsed = now - startTime
    seconds = elapsed.seconds
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    await ctx.send("Running for {}d {}h {}m {}s".format(elapsed.days, hours, minutes, seconds))

@client.command()
@commands.cooldown(1, 5)
async def userinfo(ctx, member: discord.Member): #This will get information about a user
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
async def serverinfo(ctx): #This will get information about the server
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
@commands.cooldown(1, 30)
async def find(ctx,*, query): #This will retrieve google results for a query
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
@commands.cooldown(1, 30)
@commands.check(is_owner)
async def setgame(ctx, *, game='null'): #This will set the game activity or "playing ..."
    await client.change_presence(status=discord.Status.online, activity=discord.Game(f'{game}'))
    await ctx.send(f'My game activity is now: {game}')
    print(f'My game activity is now: {game}')

    @setgame.error
    async def setgame_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'This command is on cooldown, but you can use it again in {round(error.retry_after, 2)} seconds!')

@client.command()
@commands.cooldown(1, 10)
async def snipe(ctx): #This will retrieve a recently deleted message in the channel it is used.
    channel = ctx.channel
    try: #This piece of code is run if the bot finds anything in the dictionary
        em = discord.Embed(name = f"Last deleted message in #{channel.name}", description = snipe_message_content[channel.id])
        em.set_footer(text = f'This message was sent by {snipe_message_author[channel.id]}')
        await ctx.send(embed = em)
    except: #This piece of code is run if the bot doesn't find anything in the dictionary
        await ctx.send(f"I couldn't find any recently deleted messages in #{channel.name} !")

    @snipe.error
    async def snipe_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'This command is on cooldown, but you can use it again in {round(error.retry_after, 2)} seconds!')

@client.command()
@commands.cooldown(1, 15)
@commands.check(is_owner)
async def dm(ctx, member: discord.Member=None, message=''): #This will direct message a user
  if member == None:
    await ctx.send('Mention a member, please!')
    return
  try:
      await member.send(f"{message}")
      await ctx.send(f'Message delivered to: {member}')

  except commands.CommandInvokeError:
      await ctx.send("Couldn't send message to user")

@client.command(aliagses=('serverinfo', 'host'))
@commands.cooldown(1, 30)
async def server(ctx): #This will show information about the host machine
    cpufreq = psutil.cpu_freq()
    cpuphys = psutil.cpu_count(logical=False)
    cpucores = psutil.cpu_count(logical=True)
    svmem = psutil.virtual_memory()
    uname = platform.uname()
    async with ctx.typing():
        await ctx.send(f'============== CPU =============== \n **Physical cores:** {cpuphys} \n **Total cores:** {cpucores} \n **Current Frequency:** {cpufreq.current:.2f}Mhz \n **Max Frequency:** {cpufreq.max:.2f}Mhz \n **Min Frequency:** {cpufreq.min:.2f}Mhz \n **Total CPU Usage:** {psutil.cpu_percent()}%')
        await ctx.send(f'============== Mem =============== \n **Total:** {get_size(svmem.total)} \n **Used:** {get_size(svmem.used)} \n **Percentage:** {svmem.percent}%')
        await ctx.send(f'============== Sys =============== \n **System:** {uname.system} \n **Release:** {uname.release} \n **Version:** {uname.version} \n **Machine:** {uname.machine} \n **Processor:** {uname.processor}')

@client.command(aliases=["shut", "shutdown", "quit", "stahp", "kill"])
@commands.check(is_owner)
async def stop(ctx): #This will stop the bot's process
   await ctx.send("Attention: I have been murdered.")
   await client.close()

startTime = datetime.utcnow()
tokenFile = open(realPath/r'token.txt', 'r')
realToken = tokenFile.read()
client.run(f'{realToken}')
tokenFile.close()