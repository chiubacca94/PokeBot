# Import libraries
from tinydb import TinyDB, Query
from numpy.random import choice
import numpy as np
import json
from array import array
from collections import OrderedDict


class TinyDbInterface:
    # Static variables
    poke_arr = []       # Used for choosing
    weights = []        # Used for assigning weights to respective poke_arr

    # Pokemon Name to index (need? also change this eventually)
    def Name2Index(self, PokemonNameKey):
       return int(PokemonKeyName.split(".")[1])

    # Pokemon Index to Name
    def Index2Name(self, PokemonInd):
        data = json.load(open('PokemonData.json'), object_pairs_hook=OrderedDict)

        for key,value in data.items():
            if PokemonInd in key:
                return value['name']
                #return value['name'] + "." + key

    # Increment the pokemon count in an array
    def IncrementPokeArr(self, arr, pokemonIndex):
        pokemonIndex = int(pokemonIndex)
        # print(arr)
        arr[pokemonIndex] = arr[pokemonIndex] + 1
        return arr

    # Decrement the pokemon count in an array
    def DecrementPokeArr(self, arr, pokemonCt, index):
        pokemonIndex = int(pokemonIndex)
        # print(arr)
        arr[pokemonIndex] = arr[pokemonIndex] - 1
        return arr

        
    # Convert the 'rarity' number to a probability value (0<i<1) so we can use scientific library 
    #   to pick a weighted random number/pokemon
    def ConvertToProb(self, arr):
        converted = []
        for i in arr:
            if arr[i] == 0:
                converted.append(0)
            if arr[i] == 1:
                converted.append(0.40)
            if arr[i] == 2:
                converted.append(0.20)
            if arr[i] == 3:
                converted.append(0.15)
            if arr[i] == 4:
                converted.append(0.10)
            if arr[i] == 5:
                converted.append(0.05)
            if arr[i] == 6:
                converted.append(0.02)
            if arr[i] == 7:
                converted.append(0.02)
            if arr[i] == 8:
                converted.append(0.01)

        return converted

    # Get the rarity weights
    def SetWeights(self):
        rarr = []
        prob = []
 
        #data = json.loads(open('PokemonData.json').read())
        data = json.load(open('PokemonData.json'), object_pairs_hook=OrderedDict)
        # str_data = json.dumps(data, indent=4)

        for key, value in data.items():
            if 'rarity' in value:
                rarr.append(value['rarity'])
 

        prob = self.ConvertToProb(rarr)

        return prob

    # Set pokemon arr to index integers
    def SetPokemon(self):
        arr = []
        arr = array('i',(i for i in range(0,153))) # INIT array with index

        return arr

    # Initialize a constructor
    def __init__(self):
        self.poke_arr = self.SetPokemon()
        self.weights = self.SetWeights()


    # Add user (each user is an array of 150)
    def AddUser(self, username):
        my_pokemon = [0] * 153 # Matching arr index to pokemon index (0 is disregarded)

        db = TinyDB('users.json')
        db.insert({'username': username, 'pokemon': my_pokemon})
        
        pass # RETURN: check bool


    # Add pokemon to user (pokemon and quantity)
    def AddPokemon(self, username, pokemon):
        
        db = TinyDB('users.json')
        Username = Query()
        user = db.search(Username.username == username)
        # print(pokemon)
        my_pokemon_cur = user[0]['pokemon'][pokemon]
        # print(my_pokemon_cur)
        my_pokemon_new = self.IncrementPokeArr(user[0]['pokemon'], pokemon)
        # print (my_pokemon_new)
        db.update({'pokemon': my_pokemon_new}, Username.username == username)

        pass # RETURN: check bool

    # Remove pokemon from user
    def RemovePokemon(self, username, pokemon):
        db = TinyDB('users.json')
        Username = Query()
        user = db.search(Username.username == username)
        # print(pokemon)
        my_pokemon_cur = user[0]['pokemon'][pokemon]
        # print(my_pokemon_cur)
        my_pokemon_new = self.DecrementPokeArr(user[0]['pokemon'], pokemon)
        # print (my_pokemon_new)
        db.update({'pokemon': my_pokemon_new}, Username.username == username)

        pass # RETURN: check bool


    # Trade pokemon
    def TradePokemon(self, user1, user2, pokemon1, pokemon2):
        # Add [p1]
        AddPokemon(user1, pokemon1)

        # Remove
        RemovePokemon(user2, pokemon1)

        # Add [p2]
        AddPokemon(user2, pokemon2)
        
        # Remove
        RemovePokemon(user1, pokemon2)

        pass # RETURN: check bool


    # Check pokemon quantity for one user TEST L8R
    def GetUserPokemon(self, username):
        db = TinyDB('users.json')
        data = json.load(open('PokemonData.json'), object_pairs_hook=OrderedDict)
        pokedex = ""
        User = Query()
        user = db.search(User.username == username)
        print(user)
        poke_list = user[0]['pokemon']
        print(poke_list)

        for i in range(len(poke_list)):
            if poke_list[i] != 0:
                poke_name = self.Index2Name(str(i))
                print(poke_name)
                count = poke_list[i]
                print(count)
                pokedex = pokedex +  poke_name + " : " + str(poke_list[i]) + "\r\n" 

        # RETURN: list of pokemon and quantity List: [1] = 2 (You have 2 bulbasaurs)
        return pokedex


    # Pick pokemon by "weighted random"
    def SpawnPokemon(self):
        
        rand_pokemon = np.random.choice(self.poke_arr, 1, self.weights) # I believe it changes on each call (check on this future brittany)

        # RETURN: Name of pokemon spawned (based on number generated by "random")
        return rand_pokemon[0] # Get the first element of the array returned







