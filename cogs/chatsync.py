from discord.ext import commands
import globals
import time
import os
from mclog import McLog
from mcrcon import MCRcon

# connect to server

mcr = MCRcon(host=globals.config["server-ip"], port=globals.config["server-port"], password=globals.config["server-pwd"])

class ChatSync(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.channel.id != int(globals.config["chat-channel-id"]):
            return
        if ctx.author == self.bot.user:
            return
        role_names = [role.name for role in ctx.author.roles]
        if "Minecraft 帳號聯動" in role_names:
            mcr.command(f"say <{ctx.author.name}> {ctx.content}")
            # await ctx.channel.send(f"已將訊息 `{ctx.content}` 傳送至 Minecraft 伺服器")
        else:
            await ctx.channel.send(f"你沒有權限傳送訊息至 Minecraft 伺服器，請先聯動帳號")

async def setup(bot):
    await bot.add_cog(ChatSync(bot))
    
server_status = False
while server_status == False:
    try:
        mcr.connect()
        server_status = True
        print("連線成功")
    except:
        time.sleep(1)
        print("連線失敗，重新嘗試連線...")