import discord #Discord.py
import requests #Web requests
import json #Parse json
import os #os
import pathlib #Reach files
import psutil #OS info
import platform #OS info
import random
import time
from time import gmtime, strftime
from datetime import datetime
from googlesearch import search #Google search
from discord.ext import commands, tasks #Discord.py commands
from discord.ext.commands import CommandNotFound #Discord.py errors
from discord.ext.commands.cooldowns import BucketType #Discord.py cooldowns
pathlib.Path(__file__).parent.absolute()
filePath = pathlib.Path(__file__).absolute() #Current file's path
dirPath = pathlib.Path().absolute() #Current parent's path
realPath = dirPath/r''
client = commands.Bot(command_prefix = ',', case_insensitive=True) #Prefix
print(r'◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼◼')
print(r'File        Path: ', filePath)
print(r'Directory   Path: ', dirPath)
print(r'- - - - - - - - - - - - - - - - - - - - - - - - - -')
time123 = time.strftime("[%d/%m/%Y] %H:%M:%S")
print(time123)

try:
    with open(realPath/'log.txt') as f:
        print('Found logfile')
except IOError:
    print("Creating logfile")
    open(realPath/r'log.txt', 'x')

def cooldown():
    @userinfo.error
    async def oncooldown(ctx, error):
        print(oncooldown)
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'This command is on cooldown, but you can use it again in {round(error.retry_after, 2)} seconds!')

def is_owner(ctx): #Discord user ID's granted admin permissions
    return ctx.message.author.id == 440068179994083328

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def log(content, user):
    theDate = time.strftime("[%d/%m/%Y] %H:%M:%S")
    logFile = open(realPath/r'log.txt', 'a')
    logFile.write(f'{theDate} || {user} Performed {content}\n')
    logFile.close()

#! Events

snipe_message_author = {}
snipe_message_content = {}

@client.event
async def on_message_delete(message): #Getting the messages for the snipe command
    snipe_message_author[ message.channel.id] = message.author
    snipe_message_content[message.channel.id] = message.content

@client.event
async def on_ready(): #This will execute when the bot comes online
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name='discord.py docs'))
    print(r'Started.')

@client.event 
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send('Command not recognised!')
        return
    raise error

#! Commands

@client.command()
@commands.check(is_owner)
async def newchannel(ctx, times=1, *, name=None):
    if name is None:
        ctx.send('Please provide a name!')

    log(content=f'newchannel with name={name}, times={times}', user=ctx.message.author)
    if name == "random":
        for i in range(times):
            print(i)
            randname = random.randint(100000000, 999999999)
            await ctx.message.guild.create_text_channel(randname)
    else:
        for i in range(times):
            await ctx.message.guild.create_text_channel(name)

@client.command()
@commands.check(is_owner)
async def newrole(ctx, name=None, times=1):
    if name is None:
        ctx.send('Please provide a name!')

    log(content=f'newrole with name={name}, times={times}', user=ctx.message.author)
    if name == "random":
        for i in range(times):
            print(i)
            randname = random.randint(100000000, 999999999)
            await ctx.message.guild.create_role(randname)
    else:
        for i in range(times):
            await ctx.message.guild.create_role(name)

@client.command()
@commands.cooldown(1, 5)
async def info(ctx): #This will show some information about the bot
    log(content=f'info', user=ctx.message.author)
    await ctx.send('MineKrypt\'s Assistant | Prefix: , | Made for DisRoom™ | v1.3')

@client.command(brief='Displays the invite code.', aliases=('invite', 'i'))
@commands.cooldown(1, 30)
async def inv(ctx): #This will give an invite
    log(content=f'invite', user=ctx.message.author)
    await ctx.send('Join DisRoom™! | discord.gg/7tJq6xH')

@client.command(aliases=('latency', 'p'))
@commands.cooldown(1, 5)
async def ping(ctx): #This will show the latency to discord
    log(content=f'ping', user=ctx.message.author)
    await ctx.send(f'Latency: *{round(client.latency * 1000)}ms*')

@client.command(aliases=('say', 'rpt'))
@commands.cooldown(1, 5)
async def echo(ctx, echoed): #This will repeat text
    log(content=f'echo with content={echoed}', user=ctx.message.author)
    await ctx.send(echoed)

@client.command()
@commands.cooldown(1, 5)
async def echos(ctx, echoed): #This will repeat text and delete the original command
    log(content=f'echos with content={echoed}', user=ctx.message.author)
    await ctx.message.delete()
    await ctx.send(echoed)

@client.command()
@commands.cooldown(1, 5)
async def uptime(ctx): #This will show how long the bot has been online
    log(content=f'uptime', user=ctx.message.author)
    now = datetime.utcnow()
    elapsed = now - startTime
    seconds = elapsed.seconds
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    await ctx.send("Running for {}d {}h {}m {}s".format(elapsed.days, hours, minutes, seconds))

@client.command()
@commands.cooldown(1, 5)
async def userinfo(ctx, member: discord.Member): #This will get information about a user
    log(content=f'userinfo with member={member}', user=ctx.message.author)
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
    cooldown()

@client.command()
@commands.cooldown(1, 5)
async def serverinfo(ctx): #This will get information about the server
    log(content=f'serverinfo', user=ctx.message.author)
    name = str(ctx.guild.name)
    id = str(ctx.guild.id)
    region = str(ctx.guild.region)
    memberCount = str(ctx.guild.member_count)

    icon = str(ctx.guild.icon_url)
    
    embed = discord.Embed(
        title=name + " Server Information",
        color=discord.Color.dark_red()
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Server ID", value=id, inline=True)
    embed.add_field(name="Region", value=region, inline=True)
    embed.add_field(name="Member Count", value=memberCount, inline=True)
    await ctx.send(embed=embed)
    cooldown()

@client.command(aliases=('search', 'google'))
@commands.cooldown(1, 30)
async def find(ctx,*, query):
    log(content=f'find with query={query}', user=ctx.message.author)

    author = ctx.author.mention
    await ctx.channel.send(f'Here are the links related to your question {author} ! *Query: "{query}"*')
    async with ctx.typing():
        for j in search(query, tld="com", num=3, stop=3, pause=2):
            await ctx.send(f"\n:point_right: | {j}")
    cooldown()

@client.command()
@commands.cooldown(1, 30)
@commands.check(is_owner)
async def setgame(ctx, *, game=''): #This will set the game activity or "playing ..."
    await client.change_presence(status=discord.Status.online, activity=discord.Game(f'{game}'))
    await ctx.send(f'My game activity is now: {game}')
    print(f'My game activity is now: {game}')
    cooldown()

@client.command()
@commands.cooldown(1, 10)
async def snipe(ctx): #This will retrieve a recently deleted message in the channel it is used.
    log(content=f'snipe', user=ctx.message.author)
    channel = ctx.channel
    try: #This piece of code is run if the bot finds anything in the dictionary
        em = discord.Embed(name = f"Last deleted message in #{channel.name}", description = snipe_message_content[channel.id])
        em.set_footer(text = f'This message was sent by {snipe_message_author[channel.id]}')
        await ctx.send(embed = em)
    except: #This piece of code is run if the bot doesn't find anything in the dictionary
        await ctx.send(f"I couldn't find any recently deleted messages in #{channel.name} !")
    cooldown()

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

@client.command()
@commands.cooldown(1, 30)
async def server(ctx): #This will show information about the host machine
    log(content=f'server', user=ctx.message.author)
    cpufreq = psutil.cpu_freq()
    cpuphys = psutil.cpu_count(logical=False)
    cpucores = psutil.cpu_count(logical=True)
    svmem = psutil.virtual_memory()
    uname = platform.uname()
    async with ctx.typing():
        await ctx.send(f'============== CPU =============== \n **Physical cores:** {cpuphys} \n **Total cores:** {cpucores} \n **Current Frequency:** {cpufreq.current:.2f}Mhz \n **Max Frequency:** {cpufreq.max:.2f}Mhz \n **Min Frequency:** {cpufreq.min:.2f}Mhz \n **Total CPU Usage:** {psutil.cpu_percent()}%')
        await ctx.send(f'============== Mem =============== \n **Total:** {get_size(svmem.total)} \n **Used:** {get_size(svmem.used)} \n **Percentage:** {svmem.percent}%')
        await ctx.send(f'============== Sys =============== \n **System:** {uname.system} \n **Release:** {uname.release} \n **Version:** {uname.version} \n **Machine:** {uname.machine} \n **Processor:** {uname.processor}')
    cooldown()

@client.command(aliases=["shut", "shutdown", "quit", "stahp", "kill"])
@commands.check(is_owner)
async def stop(ctx): #This will stop the bot's process
    log(content=f'stop', user=ctx.message.author)
    await ctx.send("Attention: I have been murdered.")
    await client.close()

@client.command()
async def socks(ctx):
    log(content='socks', user=ctx.message.author)
    await ctx.send('https://www.amazon.com/ZANZEA-Womens-Stocking-Striped-Tights/dp/B00OAXERZW?th=1')

@client.command()
async def eightball(ctx, *, query=None):
    log(content=f'eightball with query={query}', user=ctx.message.author)
    randCat = random.randint(1, 3)
    if randCat == 1:
        randChoice = random.randint(1, 10)
        if randChoice == 1:
            await ctx.send(f'> {query} \nIt is certain')
        elif randChoice == 2:
            await ctx.send(f'> {query} \nWithout a doubt')
        elif randChoice == 3:
            await ctx.send(f'> {query} \nYou may rely on it')
        elif randChoice == 4:
            await ctx.send(f'> {query} \nYes definitely')
        elif randChoice == 5:
            await ctx.send(f'> {query} \nIt is decidedly so')
        elif randChoice == 6:
            await ctx.send(f'> {query} \nAs I see it, yes')
        elif randChoice == 7:
            await ctx.send(f'> {query} \nMost likely')
        elif randChoice == 8:
            await ctx.send(f'> {query} \nYes')
        elif randChoice == 9:
            await ctx.send(f'> {query} \nOutlook good')
        elif randChoice == 10:
            await ctx.send(f'> {query} \nSigns point to yes')
    elif randCat == 2:
        randChoice = random.randint(1, 5)
        if randChoice == 1:
            await ctx.send(f'> {query} \nReply hazy try again')
        elif randChoice == 2:
            await ctx.send(f'> {query} \nBetter not tell you now')
        elif randChoice == 3:
            await ctx.send(f'> {query} \nAsk again later')
        elif randChoice == 4:
            await ctx.send(f'> {query} \nCannot predict now')
        elif randChoice == 5:
            await ctx.send(f'> {query} \nConcentrate and ask again')
    elif randCat == 3:
        randChoice = random.randint(1, 5)
        if randChoice == 1:
            await ctx.send(f'> {query} \nDon’t count on it')
        elif randChoice == 2:
            await ctx.send(f'> {query} \nOutlook not so good')
        elif randChoice == 3:
            await ctx.send(f'> {query} \nMy sources say no')
        elif randChoice == 4:
            await ctx.send(f'> {query} \nVery doubtful')
        elif randChoice ==5:
            await ctx.send(f'> {query} \nMy reply is no')
    

#TODO: Fix this CRAP
# @client.command()
# @commands.check(is_owner)
# async def logs(lines=10)
#     total_lines_wanted = lines

#     BLOCK_SIZE = 1024
#     f.seek(0, 2)
#     block_end_byte = f.tell()
#     lines_to_go = total_lines_wanted
#     block_number = -1
#     blocks = []
#     while lines_to_go > 0 and block_end_byte > 0:
#         if (block_end_byte - BLOCK_SIZE > 0):
#             f.seek(block_number*BLOCK_SIZE, 2)
#             blocks.append(f.read(BLOCK_SIZE))
#         else:
#             f.seek(0,0)
#             blocks.append(f.read(block_end_byte))
#         lines_found = blocks[-1].count(b'\n')
#         lines_to_go -= lines_found
#         block_end_byte -= BLOCK_SIZE
#         block_number -= 1
#     all_read_text = b''.join(reversed(blocks))
#     return b'\n'.join(all_read_text.splitlines()[-total_lines_wanted:])

startTime = datetime.utcnow()
tokenFile = open(realPath/r'token.txt', 'r')
realToken = tokenFile.read()
client.run(f'{realToken}')
tokenFile.close()