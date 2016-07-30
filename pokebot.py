# =====================================================================================================================================================
# Pokebot will randomly have pokemon appear in chats.
#   Only 151 are here
# ** MUST HAVE pyTelegramBotAPI : [pip install pyTelegramBotAPI] or upgrade [pip install pytelegrambotapi --upgrade]
# ** MUST HAVE tinydb : [pip install tinydb] and scipy [pip install scipy] need numpy
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

# Allow communication between functions here idk...
global curPokemon
global curPokemonNum
global active

# init
curPokemon = ''
curPokemonNum = ''
active = False

# Frequency of a pokemon appearing
f = 0.80

# Message handler for /start and /help
@bot.message_handler(commands=['help'])
def send_welcome(message):

    bot.reply_to(message, "Catch the pokemon when they appear!")


# Message handler for when a user will /join the pokemon ...quest? .......
@bot.message_handler(commands=['join'])
def join_action(message):
    db = TinyDbInterface()
    
    # cannot join 2x!!!
    if(db.CheckUserExists(message.from_user.username) == 0):
        bot.reply_to(message, "You already joined!")
    else:
        db.AddUser(message.from_user.username)
        print(message.from_user.username)
        bot.reply_to(message, "Welcome to the World of Pokemon " + message.from_user.username)


# Message handler for when a user will /catch a pokemon
@bot.message_handler(commands=['catch'])
def send_catch_action(message):
    db = TinyDbInterface()
    global active

    print("Caught: " + curPokemon)
    print(curPokemonNum)
    
    if curPokemonNum == '':
        print("No pokemon to catch :(")
        bot.reply_to(message, "Nothing is there :(")
    else:
        if(db.CheckUserExists(message.from_user.username) == 0):
            if(active==True):
                db.AddPokemon(message.from_user.username, int(curPokemonNum))
                active = False
                bot.reply_to(message, message.from_user.username + " caught a " + curPokemon)
            else: 
                bot.reply_to(message, "Nothing is there.") 
        else:
            bot.reply_to(message, "Who are you?")
   
    pass


# Message handler for when a user will /check all pokemon
@bot.message_handler(commands=['pokedex'])
def send_pokedex_action(message):
    pokedex = ''
    db = TinyDbInterface()
    
    if(db.CheckUserExists(message.from_user.username) == 0):
        pokedex = db.GetUserPokemon(message.from_user.username)
        if(pokedex != ""):
            bot.reply_to(message, pokedex)
            bot.sendChatAction(message['chat']['id'], 'upload_photo')
            bot.sendPhoto(message['chat']['id'], open('user_dex.png', 'rb'), caption(pokedex))
        else:
            bot.reply_to(message, "You have no pokemon.")
    else:
        bot.reply_to(message, "Who are you?")

    pass


# Message handler for random pokemon spawning
# @bot.message_handler(func=lambda m: (random.random() < f)) # Return less than not equal to 1 #yaySTAT
@bot.message_handler(commands=['spawn'])
def appear(message):
    db = TinyDbInterface()
    global curPokemon
    global curPokemonNum
    global active
    
    while True:
        pokemon = db.SpawnPokemon()
        int(pokemon)
        curPokemonNum = pokemon
        pokemon = str(pokemon)
        pokemon_name = db.Index2Name(pokemon)
        curPokemon = pokemon_name
        active = True

        if curPokemon != 'none':
                break

    print(curPokemon)
    print(curPokemonNum)
    bot.reply_to(message, curPokemon + " has appeared!")
    # bot.send_message(message.chat.id, curPokemon + " has appeared!")


# Bot waits for events
print("Pokebot is running...")
bot.polling()
