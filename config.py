import os
from dotenv import load_dotenv

load_dotenv()

# Discord Bot
TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = "!"

# Banco de dados
DATABASE = "asc_bot.db"

# Configurações de treino
TRAINING_EVENTS = {
    1: {
        "name": "Bom treino!",
        "over_gain": 0,
        "description": "Não evolui nada no overall",
        "weight": 20,  # 20% de chance
        "rarity": "common"
    },
    2: {
        "name": "Grande Treino!",
        "over_gain": 2,
        "description": "Evolui +2 de over",
        "weight": 15,
        "rarity": "uncommon"
    },
    3: {
        "name": "Lesão Leve",
        "over_gain": 0,
        "description": "1 jogo sem jogar",
        "weight": 20,
        "rarity": "common",
        "injury": True,
        "games_out": 1
    },
    4: {
        "name": "Lesão Média",
        "over_gain": 0,
        "description": "Meia temporada sem jogar",
        "weight": 18,
        "rarity": "uncommon",
        "injury": True,
        "games_out": 38  # ~metade de uma temporada
    },
    5: {
        "name": "Lesão Grave",
        "over_gain": 0,
        "description": "1 temporada sem jogar",
        "weight": 12,
        "rarity": "rare",
        "injury": True,
        "games_out": 76  # temporada completa
    },
    6: {
        "name": "Treino perfeito!",
        "over_gain": 3,
        "description": "+3 de over",
        "weight": 15,
        "rarity": "epic"
    }
}

# Configurações de XP
XP_PER_MESSAGE = 5
XP_PER_VOICE_MINUTE = 0.5
MESSAGE_COOLDOWN = 60  # segundos entre mensagens que dão XP

# Level Up
def get_xp_for_level(level):
    """Calcula XP necessário para atingir um nível"""
    return 100 * level

# Over/Potential
OVER_MIN = 50
OVER_MAX = 70
POTENTIAL_MIN = 75
POTENTIAL_MAX = 90