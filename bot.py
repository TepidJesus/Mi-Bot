import discord
from dotenv import load_dotenv
import os

from message_analyzer import Message_processor

message_handler = Message_processor()


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
miBot = discord.Bot()
miBot.intents.all()

@miBot.slash_command() # Just A Test Command
async def hello(ctx):
    await ctx.respond('Hello')

@miBot.event
async def on_ready():
        print(f'[INFO] Mi Bot Has Connected To Discord...')

@miBot.event()
async def on_message(message):
    if message.author == miBot.user:
        return
    else:
        message_as_list = message_handler.listify_message(message_raw=message)
        if message_handler.swear_check(message_as_list):
            


miBot.run(TOKEN)