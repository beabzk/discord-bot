import requests
import os
import dotenv
import discord
from discord.ext import commands, tasks
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import requests

dotenv.load_dotenv()

weatherapi = os.environ.get('WEATHERAPI_KEY')
bot_token = os.environ.get('BOT_TOKEN')

intents = discord.Intents.default()
intents.typing = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

api_url = f'https://api.weatherapi.com/v1'

try:
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        print("API response:", data)
    else:
        print("API request failed with status code:", response.status_code)
        print("Error message:", response.text)
except requests.exceptions.RequestException as e:
    print("An error occurred:", e)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    send_weather_message.start()

@tasks.loop(hours=1)
async def send_weather_message():
    response = requests.get(f'{api_url}/current.json?key={weatherapi}&q=Addis Ababa')
    data = response.json()

    channel_id = 1171722910956797992
    channel = bot.get_channel(channel_id)

    if channel:
        weather_info = f"Current temperature: {data['current']['temp_c']}°C, Condition: {data['current']['condition']['text']}"
        await channel.send(f'Current weather in Addis Ababa: {weather_info}')
    else:
        print(f"Channel with ID {channel_id} not found.")

@bot.command()
async def start(ctx):
    """
    Start hourly weather updates.
    """
    if not send_weather_message.is_running():
        send_weather_message.start()
        await ctx.send('Hourly weather updates started.')
    else:
        await ctx.send('Hourly weather updates are already running.')

@bot.command()
async def stop(ctx):
    """
    Stop hourly weather updates.
    """
    if send_weather_message.is_running():
        send_weather_message.stop()
        await ctx.send('Hourly weather updates stopped.')
    else:
        await ctx.send('Hourly weather updates are not running.')

bot.remove_command('help')

@bot.command()
async def help(ctx):
    """
    Get this help message
    """
    help_embed = discord.Embed(
        title="Bot Commands",
        description="Here are the available commands:",
        color=discord.Color.blue()
    )

    for command in bot.commands:
        if not command.hidden:
            help_embed.add_field(name=f"!{command.name}", value=command.help, inline=False)

    help_embed.set_footer(text=f"Requested by {ctx.author.display_name}")
    await ctx.send(embed=help_embed)

@bot.command()
async def weather(ctx, city="Addis Ababa"):
    """
    Get the current weather for a specified location.
    Usage: `!weather [city]`
    Use "" for city names that have space in them. E.g. `!weather "New Delhi"`
    """
    response = requests.get(f'{api_url}/current.json?key={weatherapi}&q={city}')
    data = response.json()

    if response.status_code == 200:
        weather_info = f"Current temperature: {data['current']['temp_c']}°C, Condition: {data['current']['condition']['text']}"
        await ctx.send(f'Current weather in {city}: {weather_info}')
    else:
        await ctx.send(f"Failed to fetch weather data for {city}. Check your location or try again later.")

bot.run(bot_token)