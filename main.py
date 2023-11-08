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
intents.typing = False
intents.presences = False

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
    if not send_weather_message.is_running():
        send_weather_message.start()
        await ctx.send('Hourly weather updates started.')
    else:
        await ctx.send('Hourly weather updates are already running.')

@bot.command()
async def stop(ctx):
    if send_weather_message.is_running():
        send_weather_message.stop()
        await ctx.send('Hourly weather updates stopped.')
    else:
        await ctx.send('Hourly weather updates are not running.')

bot.run(bot_token)
