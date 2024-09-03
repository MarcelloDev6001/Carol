import discord
import json
import __main__ as main

def is_log_enabled():
    return True

def get_discord_intents():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.typing = True
    intents.voice_states = True
    intents.members = True
    return intents

def get_points():
    pontos = {}
    try:
        with open("data/points.json", 'r') as f:
            pontos = json.load(f)
    except FileNotFoundError:
        pontos = {}

    return pontos

def save_points(author: int, guild: int):
    main.points.get(str(guild), {})[str(author)] = main.points.get(str(guild), {}).get(str(author), 0) + 100
    with open("data/points.json", 'w') as f:
        json.dump(main.points, f, indent=4)

def get_level_and_xp():
    experience_membros = {}
    try:
        with open("data/XP.json", 'r') as f:
            experience_membros = json.load(f)
    except FileNotFoundError:
        experience_membros = {}
    return experience_membros

def get_json_file(path=""):
    json_dat = {}
    try:
        with open(f"data/{path}.json", 'r', encoding='utf-8') as f:
            json_dat = json.load(f)
    except FileNotFoundError:
        print(f"Json not found: {path}")
        json_dat = {}
    return json_dat

def get_text_map_from_json(json_file, guild_id=0):
    try:
        with open(f"data/{json_file}.json", 'r') as f:
            text_file = json.load(f)
            if text_file.get(guild_id, False) == False:
                return text_file["default"]
            else:
                return text_file[guild_id]
    except FileNotFoundError:
        return {}

# class CharacterLore():
#     def __init__(self) -> None:
#         self.name = ""
#         self.outfit = ""
#         self.objectives = ""
#         self.personality = ""
#         self.aliases = "",
#         self.weapon = "",
#         self.abilities = {},
#         self.extras = []

#     def from_json(self):
#         json_file = get_json_file("Lore")
#         self.name = json_file["name"]
#         self.outfit = json_file["outfit"]
#         self.objectives = json_file["objectives"]
#         self.personality = json_file["personality"]
#         self.aliases = json_file["aliases"]
#         self.weapon = json_file["weapon"]
#         self.abilities = json_file["abilities"]
#         self.extras = json_file["extras"]
#         return self