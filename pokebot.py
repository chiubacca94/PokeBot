# =====================================================================================================================================================
# Pokebot will randomly have pokemon appear in chats.
#   Only 151 are here
# ** MUST HAVE pyTelegramBotAPI : [pip install pyTelegramBotAPI] or upgrade [pip install pytelegrambotapi --upgrade]
# ** MUST HAVE tinydb : [pip install tinydb] and numpy : [pip install numpy]
# How to run: python3 pokebot.py 
# recommend: using a virtual environment
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
f = 0.05

# Message handler for /start and /help
@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.reply_to(message, "Catch the pokemon when they appear!")


# Message handler for when a user will /join the pokemon ...quest? .......
@bot.message_handler(commands=['join'])
def join_action(message):
    db = TinyDbInterface()
    
    if(type(message.from_user.username) is not str):
        username = str(message.from_user.username)
        chatid = message.chat.id
    else:
        username = message.from_user.username
        chatid = message.chat.id

    # cannot join 2x!!!
    if(db.CheckUserExists(username, chatid) == 0):
        bot.reply_to(message, "You already joined!")

    else:
        db.AddUser(username, chatid)
        print(username)
        bot.reply_to(message, "Welcome to the World of Pokemon " + username)


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

        username = message.from_user.username
        chatid = message.chat.id

        if(type(message.from_user.username) is not str):
            username = str(message.from_user.username)
            chatid = str(message.chat.id)
            # You need a username now

        if(db.CheckUserExists(username, chatid) == 0):
            if(active==True):
                db.AddPokemon(username, chatid, int(curPokemonNum))
                active = False

                bot.reply_to(message, username + " caught a " + curPokemon)
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

    username = message.from_user.username
    chatid = message.chat.id

    if(type(message.from_user.username) is not str):
        username = str(message.from_user.username)
        chatid = str(message.chat.id)

    if(db.CheckUserExists(username, chatid) == 0):
        pokedex = db.GetUserPokemon(username, chatid)
        if(pokedex != ""):
            bot.reply_to(message, pokedex)
        else:
            bot.reply_to(message, "You have no pokemon.")
    else:
        bot.reply_to(message, "Who are you?")

    pass


# Message handler for when a user will /join the pokemon ...quest? .......
@bot.message_handler(commands=['spawn'])
def force_appear(message):
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
    # bot.reply_to(message, curPokemon + " has appeared!")
    bot.send_message(message.chat.id, curPokemon + " has appeared!")



# Message handler for random pokemon spawning
@bot.message_handler(func=lambda m: (random.random() < f)) # Return less than not equal to 1 #yaySTAT
# @bot.message_handler(commands=['spawn'])
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
    # bot.reply_to(message, curPokemon + " has appeared!")
    bot.send_message(message.chat.id, curPokemon + " has appeared!")


# Bot waits for events
print("Pokebot is running...")
bot.polling()
