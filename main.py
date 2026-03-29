import discord
from discord.ext import commands, tasks
from config import TOKEN, PREFIX
import os
import asyncio

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Bot
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Bot conectado como {bot.user}')
    
    # Carrega todas as cogs
    await load_cogs()

async def load_cogs():
    """Carrega todas as cogs do diretório cogs/"""
    cogs_dir = 'cogs'
    
    if not os.path.exists(cogs_dir):
        os.makedirs(cogs_dir)
    
    for filename in os.listdir(cogs_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            cog_name = filename[:-3]
            try:
                await bot.load_extension(f'cogs.{cog_name}')
                print(f'✅ Cog {cog_name} carregada')
            except Exception as e:
                print(f'❌ Erro ao carregar cog {cog_name}: {e}')

@bot.event
async def on_message(message):
    """Evento de mensagem para XP"""
    if message.author == bot.user:
        return
    
    from database import Database
    from config import XP_PER_MESSAGE, MESSAGE_COOLDOWN
    import time
    
    db = Database()
    user_id = message.author.id
    
    # Verifica se é comando
    if message.content.startswith(PREFIX):
        await bot.process_commands(message)
        return
    
    # Cria usuário se não existir
    if not db.user_exists(user_id):
        db.create_user(user_id, message.author.name, str(message.author.avatar))
    
    # Adiciona XP
    level_up, new_level = db.add_xp(user_id, XP_PER_MESSAGE)
    
    if level_up:
        await message.channel.send(
            f"🎉 Parabéns {message.author.mention}! Você subiu para o level **{new_level}**!"
        )
    
    await bot.process_commands(message)

@bot.event
async def on_voice_state_update(member, before, after):
    """Evento para XP em call"""
    from database import Database
    from config import XP_PER_VOICE_MINUTE
    
    db = Database()
    user_id = member.id
    
    # Cria usuário se não existir
    if not db.user_exists(user_id):
        db.create_user(user_id, member.name, str(member.avatar))
    
    # Se conectou em call
    if before.channel is None and after.channel is not None:
        print(f"{member.name} entrou em uma call")
    
    # Se saiu de call
    if before.channel is not None and after.channel is None:
        print(f"{member.name} saiu de uma call")

if __name__ == '__main__':
    bot.run(TOKEN)