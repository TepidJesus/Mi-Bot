import discord
from dotenv import load_dotenv
import os



load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
miBot = discord.Bot()
miBot.intents.all()

@miBot.slash_command()
async def hello(ctx):
    await ctx.respond('Hello')

@miBot.event
async def on_ready():
        print(f'[INFO] Mi Bot Has Connected To Discord...')

miBot.run(TOKEN)