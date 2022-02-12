import discord
from dotenv import load_dotenv
import os
from discord.ext import commands

from message_analyzer import Message_processor
from score_keeper import ScoreKeeper
message_handler = Message_processor()
score_handler = ScoreKeeper()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
miBot = commands.Bot(intents = discord.Intents.all())

@miBot.slash_command() # Just A Test Command
async def hello(ctx):
    await ctx.respond('Hello')

@miBot.slash_command(name='showcounts')
async def showscores(ctx):
    message_embed = (discord.Embed(color=discord.Colour.brand_red(), type='rich', title='Test'))
    await ctx.respond(embed=message_embed)

@miBot.event
async def on_ready():
        print(f'[INFO] Mi Bot Has Connected To Discord...')
        score_handler.refresh_scores(guild_members=miBot.get_all_members())
        print(f'[INFO] Swear Counts Loaded')

@miBot.event
async def on_message(message):
    if message.author == miBot.user:
        return
    else:
        message_as_list = message_handler.listify_message(message_raw=message)
        num_swear_words = message_handler.swear_check(message_as_list)
        if  num_swear_words != 0:
            score_handler.alter_score(member_name=message.author.name, num=num_swear_words)

            


miBot.run(TOKEN)