# Weather Bot

This is a simple Discord bot built with Python that can provide current weather information. 

## Features

- Get current weather for a specified city
- Start and stop hourly weather updates for a specified channel  
- Help command to view available bot commands

## Setup

### Prerequisites

- Python 3.6 or higher
- [Discord.py](https://discordpy.readthedocs.io/en/latest/#) library
- [Requests](https://docs.python-requests.org/en/latest/) library
- [Python-dotenv](https://github.com/theskumar/python-dotenv) library
- [WeatherAPI](https://www.weatherapi.com/) API key

### Installation

1. Clone the repository
   ```
   git clone https://github.com/beabzk/discord-bot.git
   ```
2. Install dependencies

3. Create a `.env` file with your [WeatherAPI](https://www.weatherapi.com/) key and Discord bot token
   ```
   WEATHERAPI_KEY=your_api_key
   BOT_TOKEN=your_bot_token  
   ```
4. Run the bot
   ```
   python main.py
   ```

## Usage

- `!weather London` - Get current weather for London
- `!start` - Start hourly weather updates in configured channel 
- `!stop` - Stop hourly weather updates
- `!help` - View all available commands

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [WeatherAPI](https://www.weatherapi.com/) for weather data
- [Discord.py](https://discordpy.readthedocs.io/en/latest/) for Discord API wrapper
