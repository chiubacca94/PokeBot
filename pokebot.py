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
from tinydb_interface import TinyDbInterface
import random

# Parse config file to get the API key
config = configparser.ConfigParser()
config.read("pokebot.cfg")

TOKEN = config['telegram_bot_API']['API_TOKEN']

# Declare bot
bot = telebot.TeleBot(TOKEN)

# current pokemon (not safe need alternative!!!! :((()
global curPokemon
global curPokemonNum
curPokemon = ''
curPokemonNum = ''

# Frequency of a pokemon appearing
f = 0.90

# Message handler for /start and /help
@bot.message_handler(commands=['help'])
def send_welcome(message):

    bot.reply_to(message, "Catch the pokemon when they appear!")


# Message handler for when a user will /join the pokemon ...quest? .......
@bot.message_handler(commands=['join'])
def join_action(message):
    db = TinyDbInterface()
    # cannot join 2x!!!
    db.AddUser(message.from_user.username)
    print(message.from_user.username)
    bot.reply_to(message, "Welcome to the World of Pokemon " + message.from_user.username)


# Message handler for random pokemon spawning
# @bot.message_handler(func=lambda m: (random.random() < freq)) # Return less than not equal to 1 #yaySTAT
@bot.message_handler(commands=['spawn'])
def appear(message):
    db = TinyDbInterface()
    global curPokemon
    global curPokemonNum
    
    while True:
        pokemon = db.SpawnPokemon()
        int(pokemon)
        curPokemonNum = pokemon
        pokemon = str(pokemon)
        pokemon_name = db.Index2Name(pokemon)
        curPokemon = pokemon_name

        if curPokemon != 'none':
                break

    print(curPokemon)
    print(curPokemonNum)
    bot.reply_to(message, curPokemon + " has appeared!")
    #bot.send_message(message, "A wild " + pokemon_name + " has appeared!")


# Message handler for when a user will /catch a pokemon
@bot.message_handler(commands=['catch'])
def send_catch_action(message):
    db = TinyDbInterface()
    print("Caught: " + curPokemon)
    print(curPokemonNum)
    if curPokemonNum == '':
        print("No pokemon to catch :(")
    else:
        db.AddPokemon(message.from_user.username, int(curPokemonNum))
    # If empty or not registered???
    
    bot.reply_to(message, message.from_user.username + " caught a " + curPokemon)


# Message handler for when a user will /check all pokemon
@bot.message_handler(commands=['pokedex'])
def send_pokedex_action(message):
    pokedex = ''
    db = TinyDbInterface()
    pokedex = db.GetUserPokemon(message.from_user.username)
    # If empty or not registered???
    
    bot.reply_to(message, pokedex)



# Bot waits for events
print("Pokebot is running...")
bot.polling()
