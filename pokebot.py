# =====================================================================================================================================================
# Pokebot will randomly have pokemon appear in chats.
#   Only 151 are here
# ** MUST HAVE pyTelegramBotAPI : [pip install pyTelegramBotAPI] or upgrade [pip install pytelegrambotapi --upgrade]
# ** MUST HAVE tinydb : [pip install tinydb] and numpy
# How to run: python3 pokebot.py 
# =====================================================================================================================================================

# Import libs
import telebot
import configparser
from random import randint

# Parse config file to get the API key
config = configparser.ConfigParser()
config.read("pokebot.cfg")

TOKEN = config['telegram_bot_API']['API_TOKEN']

# Declare bot
bot = telebot.TeleBot(TOKEN)

# Message handler for /start and /help
@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "Catch the pokemon when they appear!")

# Bot waits for events
print("Pokebot is running...")
bot.polling()
