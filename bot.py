import os
import random as rd
import sqlite3
import discord
from discord.ext import commands

try:
    CONNECT = sqlite3.connect('gita.db')
    CURSOR = CONNECT.cursor()
except sqlite3.Error as error_db:
    print(error_db)

CHAPTERS = {1:47, 2:72, 3: 43, 4:42, 5:29, 6:47, 7:30, 8:28, 9:34, 10:42,\
    11:55, 12:20, 13:35, 14:27, 15:20, 16:24, 17:28, 18:78}

description = '''A bot to print the verses of the Srimad Bhagvad Gita'''
bot = commands.Bot(command_prefix=commands.when_mentioned, description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_message(message):
    ctx = await bot.get_context(message)
    # if ctx.command is None and ctx.invoked_with is not None:
    if ctx.command is None:
        ctx.view.undo()
        ctx.prefix = ctx.view.buffer[:ctx.view.index]
        # ctx.invoked_with = 'gita'
        ctx.command = bot.all_commands.get('gita')
    await bot.invoke(ctx)

@bot.command()
async def gita(ctx, nchapter: int, nsutra: int, nsutra_end=None):
    # args[0] the chapter, args[1] is the sutra
    # checking if the entered values are int and
    # a sutra for that number is present

    embed = discord.Embed(title="Bhagavad Gita", color=0xff9933)


    try:
        if nsutra in range(1, CHAPTERS.get(nchapter)+1):
            try:
                nsutra_end = int(nsutra_end)
                if nsutra_end > CHAPTERS.get(nchapter):
                    nsutra_end = CHAPTERS.get(nchapter)
                if nsutra_end < nsutra:
                    nsutra_end = nsutra
            except (TypeError, ValueError):
                nsutra_end = nsutra
            for sutra_num in range(nsutra, nsutra_end+1):
                sutras = fetch_sutra(nchapter, sutra_num).split(None, 1)[1]
                embed.add_field(name=f"{nchapter}:{sutra_num}", value=sutras, inline=False)


            # sutra = fetch_sutra(nchapter, nsutra)
            await ctx.send(embed=embed)

    except IndexError as error:
        print("== == ERROR 1st == ==\n")
        print(error)

def fetch_sutra(nchapter: int, nsutra: int):
    CURSOR.execute("SELECT sutra FROM sutras WHERE chapter=? AND nsutra=?", (nchapter, nsutra,))
    return ''.join(CURSOR.fetchone())

@bot.command()
async def random(ctx):
    nchapter = rd.choice(list(CHAPTERS.keys()))
    nsutra = rd.randint(1, CHAPTERS.get(nchapter))
    embed = discord.Embed(title="Bhagvad Gita", color=0xff9933)

    sutra = fetch_sutra(nchapter, nsutra).split(None, 1)[1]
    # split to remove the sholka numb from the string, removes till first space

    embed.add_field(name=f"{nchapter}:{nsutra}", value=sutra, inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def info(ctx):
    embed = discord.Embed(title="Sanjaya", description="A Discord Bot for Bhagavad Gita", color=0xeee657)
    
    embed.add_field(name="Author", value="Greed#1924")
    embed.add_field(name="Server count", value=f"{len(bot.guilds)}")
    embed.add_field(name="Invite", value="[Invite link](https://discordapp.com/api/oauth2/authorize?client_id=413033214836342794&permissions=2048&scope=bot)")

    await ctx.send(embed=embed)

bot.remove_command('help')

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Sanjaya", description="A Discord Bot for Bhagavad Gita. List of commands:", color=0xeee657)
    embed.add_field(name="@Sanjaya X Y", value="Prints the Verse number **Y** from Chapter number **X**", inline=False)
    embed.add_field(name="@Sanjaya X Y Z", value="Prints the Verses from number **Y** till **Z** from Chapter number **X**", inline=False)
    embed.add_field(name="@Sanjaya random", value="Prints a random verse from Bhagavad Gita.", inline=False)
    embed.add_field(name="@Sanjaya help", value="Prints this message.", inline=False)
    await ctx.send(embed=embed)

bot.run(os.environ.get('BOT_TOKEN', None))

CONNECT.close()
