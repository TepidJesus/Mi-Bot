import discord
from dotenv import load_dotenv
import os
from discord.ext import commands

from message_analyzer import Message_processor
from score_keeper import ScoreKeeper
from quote_keeper import QuoteKeeper
message_handler = Message_processor()
score_handler = ScoreKeeper()
quote_handler = QuoteKeeper()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
miBot = commands.Bot(intents = discord.Intents.all())

@miBot.slash_command(name='highscores') # Replies with the top 3 highest scores in the server
async def showscores(ctx):
    top_scores = list()
    top_scores = score_handler.get_top_three()
    message_embed = discord.Embed(title="Top Three Swear Counts In The Server", color=0x00aaff)
    message_embed.set_author(name=miBot.user.name)
    message_embed.add_field(name=f"🟨 - {top_scores[0][0]}", value=f'{top_scores[0][1]} Points', inline=True)
    message_embed.add_field(name=f"⬜ - {top_scores[1][0]}", value=f'{top_scores[1][1]} Points', inline=False)
    message_embed.add_field(name=f"🟫 - {top_scores[2][0]}", value=f'{top_scores[2][1]} Points', inline=False)
    message_embed.set_footer(text='To See Your Own Score Use  /myscore')
    await ctx.respond(embed=message_embed)

@miBot.slash_command(name='myscore')
async def myscore(ctx):
    member = ctx.author.name
    member_score = score_handler.get_member_score(member_name=member)
    message_embed = discord.Embed(color=0x00aaff)
    message_embed.add_field(name=f'Your Current Score Is:', value=f"{member_score} Points", inline=True)
    await ctx.respond(embed = message_embed)

quotes = miBot.create_group(name="quotes", description="testing", guild_ids=[927423272033865841,])

@quotes.command(name= 'add')
async def myscore(ctx, user: discord.Option(str, "The Name Of The User You Wish To Quote", required=True, default='Nothing Entered')):
    c_channel = miBot.get_channel(ctx.channel.id)
    messages = await c_channel.history(limit=25).flatten()
    cached_message = str()
    for message in messages:
        if message.content != '' and message.author.name == user:
            cached_message = message.content
            cached_message = '"' + cached_message + '"'
            break
    quote_handler.add_quote(quote=cached_message, member=ctx.author.name)
    await ctx.respond('Command Run Fully')

@quotes.command(name='show')
async def show_member_quotes(inter: discord.Interaction):
    pass # Place Holding...

@miBot.event
async def on_ready():
        print(f'[INFO] Mi Bot Has Connected To Discord...')
        score_handler.refresh_scores(guild_members=miBot.get_all_members())
        print(f'[INFO] Swear Counts Loaded')
        quote_handler.refresh_quotes(guild_members=miBot.get_all_members())
        print(f'[INFO] Quotes Loaded')

@miBot.event
async def on_message(message):
    if message.author == miBot.user:
        return
    else:
        message_as_list = message_handler.listify_message(message_raw=message)
        num_swear_words = message_handler.swear_check(message_as_list)
        if  num_swear_words != 0:
            score_handler.alter_score(member_name=message.author.name, num=num_swear_words)


miBot.add_application_command(quotes)
miBot.run(TOKEN)