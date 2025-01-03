import discord
from discord.ext import commands
import os
import random
import asyncio
from pymongo import MongoClient

description = '''Isbjorn Support Bot'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', description=description, intents=intents)

# MongoDB setup
mongo_client = MongoClient(os.getenv("MONGODB_URI"))
db = mongo_client['discord_bot']
user_collection = db['users']

churchill_facts = [
    "Churchill is known as the 'Polar Bear Capital of the World'.",
    "Churchill is located on the western shore of Hudson Bay.",
    "The town is accessible only by plane or train."
]

polar_bear_facts = [
    "Polar bears are the largest land carnivores in the world.",
    "Polar bears have black skin under their white fur.",
    "Polar bears can swim for several days without rest."
]

snowboarding_facts = [
    "Snowboarding became an Olympic sport in 1998.",
    "The first snowboard was invented in 1965 and was called a 'Snurfer'.",
    "Shaun White is one of the most famous snowboarders in the world."
]

user_data = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_member_join(member):
    welcome_channel = discord.utils.get(member.guild.channels, name='welcome')
    if welcome_channel:
        await welcome_channel.send(f'Welcome to the server, {member.mention}! We are glad to have you here. Feel free to ask any questions about Churchill, polar bears, or snowboarding.')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if 'churchill' in message.content.lower():
        fact = random.choice(churchill_facts)
        await message.channel.send(f'Churchill Fact: {fact}')
    if 'polar bear' in message.content.lower():
        fact = random.choice(polar_bear_facts)
        await message.channel.send(f'Polar Bear Fact: {fact}')
    if 'snowboarding' in message.content.lower():
        fact = random.choice(snowboarding_facts)
        await message.channel.send(f'Snowboarding Fact: {fact}')
    await bot.process_commands(message)

@bot.command()
async def info(ctx):
    await ctx.send('This bot provides information about the town of Churchill, polar bears, and snowboarding. It also includes a fun snowboarding minigame!')

@bot.command()
async def trivia(ctx):
    category = random.choice(['churchill', 'polar_bear', 'snowboarding'])
    if category == 'churchill':
        fact = random.choice(churchill_facts)
        await ctx.send(f'Churchill Fact: {fact}')
    elif category == 'polar_bear':
        fact = random.choice(polar_bear_facts)
        await ctx.send(f'Polar Bear Fact: {fact}')
    else:
        fact = random.choice(snowboarding_facts)
        await ctx.send(f'Snowboarding Fact: {fact}')

@bot.command()
async def jump(ctx):
    user_id = ctx.author.id
    if user_id not in user_data:
        user_data[user_id] = {"points": 0, "achievements": [], "items": [], "last_jump": None}
    
    last_jump = user_data[user_id]["last_jump"]
    if last_jump and (discord.utils.utcnow() - last_jump).total_seconds() < 600:
        await ctx.send('You need to wait 10 minutes before jumping again.')
        return
    
    user_data[user_id]["last_jump"] = discord.utils.utcnow()
    points = random.randint(1, 10)
    user_data[user_id]["points"] += points
    await ctx.send(f'You jumped over an obstacle and earned {points} points! Total points: {user_data[user_id]["points"]}')
    await ctx.send('You have 10 seconds to perform tricks before landing. Type `!trick` to perform tricks.')

    await asyncio.sleep(10)
    await ctx.send('You have landed!')

@bot.command()
async def trick(ctx):
    user_id = ctx.author.id
    if user_id not in user_data or user_data[user_id]["last_jump"] is None:
        await ctx.send('You need to jump first by typing `!jump`.')
        return
    
    if (discord.utils.utcnow() - user_data[user_id]["last_jump"]).total_seconds() > 10:
        await ctx.send('You can only perform tricks within 10 seconds after jumping.')
        return
    
    points = random.randint(5, 20)
    user_data[user_id]["points"] += points
    await ctx.send(f'You performed a trick and earned {points} points! Total points: {user_data[user_id]["points"]}')

# Get the token from the environment variable
token = os.getenv("DISCORD_TOKEN")
if token is None:
    raise ValueError("No DISCORD_TOKEN found in environment variables.")
bot.run(token)