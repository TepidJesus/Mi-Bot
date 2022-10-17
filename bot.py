import discord
from dotenv import load_dotenv
import os
import asyncio
from discord.ext import commands, tasks
import datetime

from modules.music_tracker import YTDLSource
from modules.music_tracker import MusicHandler
from modules.message_analyzer import Message_processor
from modules.score_keeper import ScoreKeeper
from modules.quote_keeper import QuoteKeeper
from modules.database_manager import DataManager
from modules.activity_monitor import ActivityMonitor

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True
intents.guild_messages = True
intents.presences = True
miBot = commands.Bot(intents = intents)

message_handler = Message_processor()
music_handler = MusicHandler()
data_manager = DataManager()
###### HELPER FUNCTIONS ######

def get_user_object(user_name):
    user_obj = miBot.get_guild(miBot.guilds[0].id).get_member_named(user_name)
    return user_obj

def get_roles(user_obj):
    try:
        user_roles = user_obj.roles[1:]
    except discord.HTTPException:
        user_roles = user_obj.roles[0]
    return user_roles

async def idle_check():
    while True:
        await asyncio.sleep(180)
        if len(music_handler.play_queue) == 0 and len(miBot.voice_clients) == 1:
            await miBot.voice_clients[0].disconnect()

######## COMMANDS ########

@miBot.slash_command(name="info", description="Request Info About A User")
async def show_user_info(ctx, user: discord.Option(str, "The Name Of The User You Would Like Info About", required=True, default=None)):
    await ctx.defer()
    if user == None:
        user_dis = ctx.author
    else: 
        user_dis = get_user_object(user_name=user)
    if user_dis == None:
        message_embed = discord.Embed(title=f"That User Doesn\'t Exist...", color=0x00aaff)
        await ctx.respond(embed=message_embed, ephemeral=True)
        return None

    user_roles = get_roles(user_dis)
    created_at = int(user_dis.created_at.timestamp())
    joined_at = int(user_dis.joined_at.timestamp())

    message_embed = discord.Embed(title=f"Information About: __{user_dis.display_name}__", color=0x00aaff)
    message_embed.add_field(name=f'Created Account:', value=f"<t:{created_at}:d>\n(<t:{created_at}:R>)", inline=True)
    message_embed.add_field(name=f'Joined Server:', value=f"<t:{joined_at}:d>\n(<t:{joined_at}:R>)", inline=True)
    message_embed.add_field(name=f'Current Roles:', value=", ".join(r.mention for r in user_roles), inline=False)
    message_embed.set_footer(text=f'Requested By {ctx.author.name}')
    message_embed.set_thumbnail(url=user_dis.avatar)

    await ctx.respond(embed=message_embed)

@miBot.slash_command(name="activity", description="Request Activity Of A User")
async def show_user_activity(ctx, user: discord.Option(str, "The Name Of The User You Would Like The Activity Of", required=True, default=None)):
    await ctx.defer()
    if user == None:
        user_dis = ctx.author
    else: 
        user_dis = get_user_object(user_name=user)
    if user_dis == None:
        message_embed = discord.Embed(title=f"That User Doesn\'t Exist...", color=0x00aaff)
        await ctx.respond(embed=message_embed, ephemeral=True)
        return None

    member_stats = activity_handler.get_member_stats(user_dis)

    message_embed = discord.Embed(title=f"Activits Statistics For __{user_dis.display_name}__", color=0x00aaff)
    message_embed.add_field(name=f"Play Time This Week:", value=f"{member_stats[0] // 60} Hours", inline=True)
    

    await ctx.respond(embed=message_embed)

#### SWEAR COUNT SYSTEM #####
swearcount = miBot.create_group(name="swearcount", description="Base Command For The Swear Score Tracker")

@swearcount.command(name='highscores')
async def showscores(ctx):
    await ctx.defer()
    top_scores = list()
    top_scores = score_handler.get_top_three()
    
    names = []
    for i in range(len(top_scores)):
        usr_obj = miBot.guilds[0].get_member(int(top_scores[i][0]))
        names.append(usr_obj.display_name)

    message_embed = discord.Embed(title="Top Three Swear Counts In The Server", color=0x00aaff)
    message_embed.set_author(name=miBot.user.name)
    message_embed.add_field(name=f"🟨 - {names[0]}", value=f'{top_scores[0][1]} Points', inline=True)
    message_embed.add_field(name=f"⬜ - {names[1]}", value=f'{top_scores[1][1]} Points', inline=False)
    message_embed.add_field(name=f"🟫 - {names[2]}", value=f'{top_scores[2][1]} Points', inline=False)
    message_embed.set_footer(text='To See Your Own Score Use  /swearcount score')
    await ctx.respond(embed=message_embed)

@swearcount.command(name='score')
async def user_score(ctx, user: discord.Option(str, "The Name Of The User", required=False, default=None)):
    if user == None:
        user = ctx.author
    else:
        user = get_user_object(user)
    member_score = score_handler.get_member_score(user)
    if member_score == None:
        message_embed = discord.Embed(title="That User Does Not Exist", color=0x00aaff)
        await ctx.respond(embed = message_embed, ephemeral=True)
    else:
        message_embed = discord.Embed(color=0x00aaff)
        message_embed.add_field(name=f'Your Current Score Is:', value=f"{member_score} Points", inline=True)
        await ctx.respond(embed = message_embed)

#### QUOTE SYSTEM ####
quotes = miBot.create_group(name="quotes", description="Base Command For All Quote Related Requests")

@quotes.command(name= 'add', description = 'Add the previoues message of the user to their quote database.')
async def add_quote(ctx, user: discord.Option(str, "The Name Of The User You Wish To Quote", required=True, default=None)):
    print("Quote Add Command Ran")
    await ctx.defer()
    c_channel = miBot.get_channel(ctx.channel.id)
    messages = await c_channel.history(limit=25).flatten()
    cached_message = str()

    usr_obj = get_user_object(user)
    if usr_obj == None:
        message_embed = discord.Embed(title="That User Does Not Exist", color=0x00aaff)
        await ctx.respond(embed = message_embed, ephemeral=True)
        return None

    for message in messages:
        if message.content != '' and message.author == usr_obj:
            cached_message = message.content
            cached_message = '"' + cached_message + '"'
            break

    if cached_message == "":
        message_embed = discord.Embed(title="I couldn't find any recent messages from that user.", color=0x00aaff)
        await ctx.respond(embed = message_embed, ephemeral=True)
        return None
    else:
        quote_handler.add_quote(quote=cached_message, member=usr_obj)
        message_embed = discord.Embed(title="Quote Added", color=0x00aaff)
        message_embed.add_field(name=cached_message, value=f'- {usr_obj.display_name}', inline=True)

    await ctx.respond(embed=message_embed)

@quotes.command(name='show')
async def show_member_quotes(ctx, user: discord.Option(str, "The Name Of The User You Wish To See Saved Quotes For", required=False, default=None)):
    if user == None:
        user = ctx.author
    else:
        user = get_user_object(user)
    member_quotes = quote_handler.retrieve_quotes(user)
    if len(member_quotes) == 0:
        message_embed = discord.Embed(title=f"{user.display_name} Has No Quoted Messages", color=0x00aaff)
    else:
        message_embed = discord.Embed(title=f"{user.display_name}'s Quoted Messages:", color=0x00aaff)    
        for quote in member_quotes:
            message_embed.add_field(name=quote, value=f"- {user.display_name}", inline=False)
    await ctx.respond(embed=message_embed)

#### MUSIC SYSTEM ####
music = miBot.create_group(name="music", description="Commands to control MiBot's Music Function")

@music.command(name='play', description='Play the specified track via youtube search or link')
async def play_track(ctx, track: discord.Option(str, "The Name Of The Track You Wish To Play", required=True, default='Rick Roll')):
    await ctx.defer()

    if track[0:24] == 'https://www.youtube.com/':
        try:
            player = await YTDLSource.from_url(track, loop=miBot.loop, stream=True)
        except:
            message_embed = discord.Embed(description="Sorry, Something Went Wrong. Please Try Again Later.", color=0x49d706)
            await ctx.respond(embed=message_embed, ephemeral=True)
            return None
    else:
        try:
            player = await YTDLSource.from_search(track, loop=miBot.loop, stream=True)
        except:
            message_embed = discord.Embed(description="Sorry, Something Went Wrong. Please Try Again Later.", color=0x49d706)
            await ctx.respond(embed=message_embed, ephemeral=True)
            return None
    if len(music_handler.play_queue) >= 10:
        message_embed = discord.Embed(description="The Queue is Already Full. Please Try Again Soon.", color=0x49d706)
        await ctx.respond(embed=message_embed, ephemeral=True)
    elif len(music_handler.play_queue) > 0 or ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
        music_handler.queue_track((ctx, player))
        await ctx.respond(embed=music_handler.get_queued_track_embed(player.data['title'], player.data['thumbnail'],ctx.author.name))        
    else:
        music_handler.queue_track((ctx, player))
        music_handler.play_obj(ctx, player)
        await ctx.respond(embed=music_handler.get_now_playing_embed(player.data['title'], player.data['thumbnail'], ctx.author.name))
            
        
@music.command(name='resume', description='Resume A Paused Track')
async def resume_track(ctx):
    if ctx.voice_client.is_paused():
        ctx.voice_client.resume()
    else:
        message_embed = discord.Embed(description="No Track Is Currently Paused", color=0x49d706)
        await ctx.respond(embed=message_embed, ephemeral=True)

@music.command(name='skip', description='Skip the currently playing track')
async def skip_track(ctx):
    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()
    else:
        message_embed = discord.Embed(description="No Track Is Currently Playing", color=0x49d706)
        await ctx.respond(embed=message_embed, ephemeral=True)

@music.command(name='pause', description='Pause The Current Track')
async def pause_track(ctx):
    try:
        ctx.voice_client.pause()
    except:
        message_embed = discord.Embed(description="No Track Is Currently Playing", color=0x49d706)
        await ctx.respond(embed=message_embed, ephemeral=True)

@music.command(name='playing', description='Show The Current Playing Track')
async def playing(ctx):
    if ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
        await ctx.respond(embed=music_handler.get_now_playing_embed(music_handler.play_queue[-1][1].data['title'], music_handler.play_queue[-1][1].data['thumbnail'], ctx.author.name ), ephemeral=True)
    else:
        message_embed = discord.Embed(description="No Track Is Currently Playing", color=0x49d706)
        await ctx.respond(embed=message_embed, ephemeral=True)

@music.command(name='disconnect', description='Force The Bot To Disconnet')
async def bot_disconnect(ctx):
    if ctx.voice_client.is_playing():
        play_queue = []
        ctx.voice_client.stop()
    await ctx.voice_client.disconnect()
    message_embed = discord.Embed(title=f"MiBot Has Left The Channel", color=0x00aaff)
    await ctx.respond(embed=message_embed)

@play_track.before_invoke
async def ensure_voice(ctx):
    if ctx.voice_client is None:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.respond(embed=discord.Embed(description="You are not in a voice channel.", color=0x49d706), ephemeral=True)
    elif ctx.voice_client.channel != ctx.author.voice.channel:
        await ctx.voice_client.move_to(ctx.author.voice.channel)

@skip_track.after_invoke
async def check_queue(ctx):
    if len(music_handler.play_queue) <= 1:
        message_embed = discord.Embed(description="Queue Empty, Leaving The Channel", color=0x49d706)
        await ctx.respond(embed=message_embed, ephemeral=True)
        await bot_disconnect(ctx)
    else:
        await ctx.respond(embed=music_handler.get_now_playing_embed(music_handler.play_queue[-2][1].data['title'], music_handler.play_queue[-2][1].data['thumbnail'], ctx.author.name))

######## LISTENERS ########
#### BOT LISTENING EVENTS ####
@miBot.event
async def on_connect():
    print(f'[INFO] Mi Bot Has Connected To Discord...')
    global score_handler
    global quote_handler
    global activity_handler
    score_handler = ScoreKeeper(miBot.guilds[0].members, data_manager)
    quote_handler = QuoteKeeper(miBot.guilds[0].members, data_manager)
    activity_handler = ActivityMonitor(data_manager, miBot)


@miBot.event
async def on_ready():
        print(f'[INFO] Mi Bot Is Ready')

        score_handler.refresh_scores(guild_members=miBot.get_all_members())
        print(f'[INFO] Swear Counts Loaded')

        quote_handler.refresh_quotes(guild_members=miBot.get_all_members())
        print(f'[INFO] Quotes Loaded')

        miBot.loop.create_task(activity_handler.full_activity_check())
        print(f'[INFO] Initial Activity Check Complete')
        display_guild_stats.start()

@miBot.event
async def on_message(message):
    if message.author == miBot.user:
        return None
    elif message.author.bot:
        await message.add_reaction('😒')
    else:
        message_as_list = message_handler.listify_message(message_raw=message)
        num_swear_words = message_handler.swear_check(message_as_list)
        if  num_swear_words != 0:
            score_handler.alter_score(member=message.author, num=num_swear_words)

@miBot.event
async def on_member_join(member): #TODO: Ensure all refresh_XX methods are run whenver a member joins.
    if not member.bot:

        quote_handler.initialize_new_member(member)
        score_handler.initialize_new_member(member)

        created_at = int(member.created_at.timestamp())
        message_embed = discord.Embed(title=f"Everyone Welcome __{member.name}__ To The Server", color=0x00aaff, description=f'ID: {member.id}')
        message_embed.add_field(name=f'Current Roles:', value=member.roles[0].name, inline=True)
        message_embed.add_field(name=f'Created Account:', value=f"<t:{created_at}:d> (<t:{created_at}:R>)", inline=True)

        if member.avatar != None:
            message_embed.set_thumbnail(url=member.avatar)
        
        await member.guild.system_channel.send(embed=message_embed)

@tasks.loop(hours=24)
async def display_guild_stats():

    curr_day = datetime.date.today()
    if curr_day.weekday() == 0 and curr_day.day != 1 and curr_day.month != 1:
        try:
            stats = activity_handler.get_guild_stats('weekly')
            message_embed = discord.Embed(title="Weekly Activity Stats:", color=0x00aaff, description=f"----------------------------------------")
            message_embed.add_field(name=f"Last Week, You All Collectively Spent: ", value=f"{stats[0] // 60} Hours Playing Games")
            message_embed.add_field(name=f"Last Weeks Most Played Game Was:", value=f"{stats[1].name} For {stats[1].get_weekly_time() // 60} Hours")
            if stats[1].picture != None:
                message_embed.set_thumbnail(url=stats[1].picture)

            await miBot.guilds[0].system_channel.send(embed=message_embed)

            message_embed = discord.Embed(title=f"Last Weeks Most Active Member Was {stats[2][0].display_name}:", color=0x00aaff, description=f"{stats[2][0].mention}")
            message_embed.add_field(name=f"Total Active Time:", value=f"{stats[2][1] // 60} Hours")
            message_embed.add_field(name=f"Their Most Played Game Was: ", value=f"{stats[2][2].name} for {stats[2][2].get_weekly_time() // 60} Hours", inline=True)
            if stats[2][2].picture != None:
                message_embed.set_thumbnail(url=stats[2][2].picture)
            elif stats[2][0].avatar == None:
                message_embed.set_thumbnail(url=stats[2][0].avatar)

            activity_handler.move_weekly_to_monthly()

            await miBot.guilds[0].system_channel.send(embed=message_embed)
        except:
            print(f'[ERROR] Failed To Display Stats')

    elif curr_day.day == 1 and curr_day.month != 1:
        try:
            stats = activity_handler.get_guild_stats('monthly')
            message_embed = discord.Embed(title="Monthly Activity Stats:", color=0x00aaff, description=f"----------------------------------------")
            message_embed.add_field(name=f"This Month, You All Collectively Spent: ", value=f"{stats[0] // 60} Hours Playing Games")
            message_embed.add_field(name=f"This Months Most Played Game Was:", value=f"{stats[1].name} For {stats[1].get_monthly_time() // 60} Hours")
            if stats[1].picture != None:
                message_embed.set_thumbnail(url=stats[1].picture)

            await miBot.guilds[0].system_channel.send(embed=message_embed)

            message_embed = discord.Embed(title=f"This Months Most Active Member Was {stats[2][0].display_name}:", color=0x00aaff, description=f"{stats[2][0].mention}")
            message_embed.add_field(name=f"Total Active Time:", value=f"{stats[2][1] // 60} Hours")
            message_embed.add_field(name=f"Their Most Played Game Was: ", value=f"{stats[2][2].name} for {stats[2][2].get_monthly_time() // 60} Hours", inline=True)
            if stats[2][2].picture != None:
                message_embed.set_thumbnail(url=stats[2][2].picture)
            elif stats[2][0].avatar == None:
                message_embed.set_thumbnail(url=stats[2][0].avatar)

            activity_handler.move_monthly_to_yearly()

            await miBot.guilds[0].system_channel.send(embed=message_embed)
        except:
            print(f'[ERROR] Failed To Display Stats')
    
    elif curr_day.day == 1 and curr_day.month == 1:
        try:
            stats = activity_handler.get_guild_stats('yearly')
            message_embed = discord.Embed(title="Yearly Activity Stats:", color=0x00aaff, description=f"----------------------------------------")
            message_embed.add_field(name=f"This Year, You All Collectively Spent: ", value=f"{stats[0] // 60} Hours Playing Games")
            message_embed.add_field(name=f"This Years Most Played Game Was:", value=f"{stats[1].name} For {stats[1].get_yearly_time() // 60} Hours")
            if stats[1].picture != None:
                message_embed.set_thumbnail(url=stats[1].picture)

            await miBot.guilds[0].system_channel.send(embed=message_embed)

            message_embed = discord.Embed(title=f"This Years Most Active Member Was {stats[2][0].display_name}:", color=0x00aaff, description=f"{stats[2][0].mention}")
            message_embed.add_field(name=f"Total Active Time:", value=f"{stats[2][1] // 60} Hours")
            message_embed.add_field(name=f"Their Most Played Game Was: ", value=f"{stats[2][2].name} for {stats[2][2].get_yearly_time() // 60} Hours", inline=True)
            if stats[2][2].picture != None:
                message_embed.set_thumbnail(url=stats[2][2].picture)
            elif stats[2][0].avatar == None:
                message_embed.set_thumbnail(url=stats[2][0].avatar)

            activity_handler.move_yearly_to_total()

            await miBot.guilds[0].system_channel.send(embed=message_embed)
        except:
            print(f'[ERROR] Failed To Display Stats')


        

#### MAIN LOOP RUN ####
miBot.loop.create_task(idle_check())
miBot.run(TOKEN)

