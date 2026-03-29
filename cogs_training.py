import discord
from discord.ext import commands
from database import Database
from embeds import TrainingEmbed
from config import TRAINING_EVENTS
import random
import asyncio

class TrainingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()
    
    def _calculate_event(self):
        """Calcula qual evento ocorreu baseado nos pesos"""
        events = list(TRAINING_EVENTS.values())
        weights = [event['weight'] for event in events]
        
        chosen_event = random.choices(events, weights=weights, k=1)[0]
        
        # Encontra o ID do evento
        for event_id, event_data in TRAINING_EVENTS.items():
            if event_data['name'] == chosen_event['name']:
                return event_id, event_data
        
        return 1, TRAINING_EVENTS[1]
    
    @commands.command(name='treinar')
    async def treinar(self, ctx):
        """Realiza um treino"""
        user_id = ctx.author.id
        
        if not self.db.user_exists(user_id):
            self.db.create_user(user_id, ctx.author.name, str(ctx.author.avatar))
        
        user_data = self.db.get_user(user_id)
        
        # Verifica se pode treinar
        can_train, remaining = self.db.can_train(user_id)
        
        if not can_train:
            await ctx.send(f"❌ Você já fez 2 treinos hoje! Volte amanhã.")
            return
        
        if not user_data['overall']:
            await ctx.send("❌ Você precisa usar `!over` antes de treinar!")
            return
        
        # Verifica lesões
        injury = self.db.get_current_injury(user_id)
        
        if injury and injury['games_remaining'] > 0:
            await ctx.send(f"🩹 Você está lesionado! Ainda faltam {injury['games_remaining']} jogos para se recuperar.")
            return
        
        # Calcula evento
        event_id, event_data = self._calculate_event()
        
        over_before = user_data['overall']
        over_after = over_before + event_data['over_gain']
        
        # Verifica limite de overall
        if over_after > user_data['potential']:
            over_after = user_data['potential']
        elif over_after < 1:
            over_after = 1
        
        # Lida com evento especial "Bom treino"
        consecutive = 0
        if event_id == 1:
            consecutive = self.db.get_consecutive_good_trainings(user_id) + 1
            
            if consecutive >= 6:
                # Ganha +2 de overall adicional
                over_after += 2
                consecutive = 0  # Reseta contagem
        else:
            consecutive = 0
        
        # Adiciona lesão se aplicável
        if event_data.get('injury'):
            self.db.add_injury(user_id, event_data['name'], event_data['games_out'])
        
        # Atualiza overall
        self.db.set_overall(user_id, over_after)
        
        # Registra treino
        self.db.add_training(user_id, event_id, event_data['name'], over_before, over_after, consecutive)
        
        # Cria embed de resultado
        embed = TrainingEmbed.create_training_result_embed(
            user_data, event_data, over_before, over_after, consecutive
        )
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(TrainingCog(bot))