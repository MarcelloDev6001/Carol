import discord

GUILDS_IDS = [
    1218323333096013924,
    1221946490453360843
]

GUILDS = [
    discord.Object(id=GUILDS_IDS[0]),
    discord.Object(id=GUILDS_IDS[1])
]

GUILDS_NEWS_CHANNEL = {
    "1218323333096013924": 1226184700717043712,
    "1221946490453360843": 1221946491656994901
}

GUILDS_MAIN_CHANNEL = {
    "1218323333096013924": 1232110291320442941,
    "1221946490453360843": 1221946491656994901
}

LOG_CHANNELS = {
    1218323333096013924: 1238996437648412822
}

members = {}

membersrooms = {
    1220530296785469460: {"owner": 977009830642450532},
    1220529953490210896: {"owner": 1031987262914834463},
    1220529811735318618: {"owner": 559018258481807381},
    1220530191860891771: {"owner": 739211327826034770},
    1220529879217475584: {"owner": 722551879992606791},
    1220529688871440424: {"owner": 779727883228020756},
    1220530241114738708: {"owner": 1102595513745932369},
    1220529752335454258: {"owner": 1218305183956860930},
}
# membersrooms = {}

swearings = {
    "fdp", "filho da", "foder", "merda", "mrd", "vtnc", "vai tomar no",
    "vtnsc", "dsgrç", "disgraçado", "viado", "burro", "aids"
}

hentaiswords = [
"hent",
"rule 34",
"r34",
"ru34",
"rul34",
"rule34"
"adult",
"nsfw",
"not s",
"nots",
"bdsm",
"tentacle",
"futanari"
]

unnapropriatenames = [
"vadi",
"put",
"disgr",
"punhet",
"porn"
"vagab",
"vgab",
"vgb"
]

REACTION_NUMBERS_IDS_TO_EMOJI = {
    "0": '\U00000330\U000020E3',
    "1": '\U00000031\U000020E3',
    "2": '\U00000032\U000020E3',
    "3": '\U00000033\U000020E3',
    "4": '\U00000034\U000020E3',
    "5": '\U00000035\U000020E3',
    "6": '\U00000036\U000020E3',
    "7": '\U00000037\U000020E3',
    "8": '\U00000038\U000020E3',
    "9": '\U00000039\U000020E3',
    "10": '\U0001F4AF'
}

OPENAI_API_KEY = "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"

oneblockedmessagegifs = [
    "https://media1.tenor.com/m/mHGEqvLi5PIAAAAd/blocked-message.gif",
    "https://media1.tenor.com/m/VlddAdM7T90AAAAd/1blocked-message.gif",
    "https://media1.tenor.com/m/3WbDopX_19QAAAAC/one-blocked-message.gif",
    "https://media1.tenor.com/m/GbO6vnILRtcAAAAd/blocked-message-discord.gif",
    "https://media1.tenor.com/m/xOSRzYlsk_oAAAAC/1-blocked-message.gif",
    "https://i.pinimg.com/originals/7e/a0/25/7ea025a60f414e5ff363f1e6f2143a6e.gif",
    "https://media1.tenor.com/m/QuQiz4c0JiIAAAAd/thomas-shelby-blocked-message.gif",
    "https://media1.tenor.com/m/wwRL56gCwHQAAAAC/blocked-message-1-blocked-message.gif",
    "https://gifdb.com/images/high/blocked-message-discord-typing-coraline-movie-meme-2bov8n8q7xhi53ei.png",
    "https://media1.tenor.com/m/kBjRTg6fBj8AAAAd/1blocked-message.gif",
    "https://media1.tenor.com/m/cMZKZcMzrJYAAAAd/blocked-message.gif",
    "https://imgflip.com/gif/8alwco",
    "https://media1.tenor.com/m/GPvfUHvU3bIAAAAC/the-block-button-aint-enough-i-want-him-dead.gif",
    "https://media1.tenor.com/m/T0puJsyWDBcAAAAC/1blocked-blocked-message.gif",
    "https://media1.tenor.com/m/yu30o-BAtrAAAAAd/blocked-message.gif"
]

start_typing_time = {}
user_last_messages = {}
ARQUIVO_PONTOS = 'data/points.json'
inventario = {}

TEXTO_AUDIO_MAP = {
    "whistle": {"audio": "whistle"},
    "abobora": {"audio": "abobora"},
    "agora": {"audio": "agora"},
    "aids": {"audio": "aids"},
    "baldi": {"audio": "baldi"},
    "balls": {"audio": "ballsinurjon"},
    "777": {"audio": "brazino"},
    "byebye": {"audio": "byebye"},
    "catnap": {"audio": "catnap"},
    "party": {"audio": "discodisco"},
    "doutor": {"audio": "doutornefario"},
    "galaxybrain": {"audio": "galaxybrain"},
    "garotas-palhacas": {"audio": "garotaspalhaças"},
    "kirby": {"audio": "kirbyfalling"},
    "lula": {"audio": "lula lá ele"},
    "maxista": {"audio": "machismo"},
    "cu": {"audio": "mordecai"},
    "nhonho": {"audio": "nhonho"},
    "no-final": {"audio": "nofinal"},
    "paralelepipedo": {"audio": "paralelepipedo"},
    "pinto": {"audio": "pinto"},
    "rabo-do-gato": {"audio": "rabodogato"},
    "the-boys": {"audio": "theboys"},
    # "xamuel": {"audio": "xamuel"},
    "scream": {"audio": "randomscream"},
    "vô": {"audio": "bistecone_vo"}
    # Adicione mais textos e arquivos de áudio conforme necessário
}

ROBLOX_USERNAME_MAP = {
    "1218305183956860930": 518222881,
    "779727883228020756": 1853828340,
    "1102595513745932369": 3769191439,
    "722551879992606791": 1956128308,
    "1031987262914834463": 2651553891,
    "739211327826034770": 559575945,
    "977009830642450532": 2457232008
}

prefix = "h."
musicprefix = "m."

musicqueue = []

guildid = 1218323333096013924

ADM_ROLES = {
    1218327147152674936, 1224143232322244618, 1218327392800473168
}

ROLES_XP_MULTIPLIER = {
    1220526206999466195: 1,
    1218328547110944838: 2,
    1222910190358237235: 3,
    1220132303842312282: 4,
    1218327392800473168: 7,
    1218327147152674936: 10
}

COMMAND_RUNNING_MESSAGE = "Carol está pensando..."
DEFAULT_STATUS = "Fazendo merda..."

TOKEN = "MTIxNDk4NTIwNDk4NTI0MTYwMA.G0xBLe.AH45FdW0P1mypbccUxfhQJsBUFFz0NLDYWBD20"
