import os
import random as rd
import sqlite3
import discord
from discord.ext import commands

try:
    conn = sqlite3.connect('gita.db')
    cur = conn.cursor()
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
async def gita(ctx, nchapter:int, nsutra:int, nsutra_end=None):
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

def fetch_sutra(nchapter:int, nsutra:int):
    cur.execute("SELECT sutra FROM sutras WHERE chapter=? AND nsutra=?", (nchapter, nsutra,))
    return ''.join(cur.fetchone())

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
    ctx.send("info")

@bot.command()
async def help(ctx):
    ctx.send("help")

bot.run(os.environ.get('BOT_TOKEN', None))

conn.close()
