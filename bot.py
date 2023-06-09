import asyncio
import discord
from discord.ext import commands
import os
import globals
from mclog import McLog

globals.initialize()
intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix = globals.config["command-prefix"], intents = intents)

async def preload():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

@bot.command()
async def un(ctx, extension):
    await bot.unload_extension(f'cogs.{extension}')
    await ctx.send(f'unloaded {extension} done')

@bot.command()
async def re(ctx, extension):
    await bot.reload_extension(f'cogs.{extension}')
    print(f'reloaded {extension} done')
    await ctx.send(f'reloaded {extension} done')

@bot.command()
async def l(ctx, extension):
    await bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'loaded {extension} done')

@bot.event
async def on_ready():
    print(">>Bot is online<<")
    activity = discord.Game(globals.config["activity"])
    await bot.change_presence(activity = activity)

async def updatelog():
    await bot.wait_until_ready()
    channel = bot.get_channel(int(globals.config["chat-channel-id"]))
    mclog = McLog(globals.config["server-log-path"])
    while not bot.is_closed():
        mclog.read()
        if mclog.getConnectStatus() == True:
            await channel.send('聊天串流已連線')
        elif mclog.getConnectStatus() == False:
            await channel.send('聊天串流已中斷')
        
        player_message = mclog.getPlayerMessage()
        if player_message != None:
            await channel.send(player_message)
        
        player_join = mclog.getPlayerJoin()
        if player_join != None:
            await channel.send(f'{player_join} 加入了伺服器')
        
        player_left = mclog.getPlayerLeft()
        if player_left != None:
            await channel.send(f'{player_left} 離開了伺服器')
        
        await asyncio.sleep(1)

async def main():
    async with bot:
        bot.loop.create_task(updatelog())
        await preload()
        await bot.start(globals.config["token"])

asyncio.run(main())