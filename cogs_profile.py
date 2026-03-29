import discord
from discord.ext import commands
from database import Database
from embeds import CareerEmbed
from config import PREFIX
import asyncio

class ProfileCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()
    
    @commands.command(name='perfil', aliases=['profile'])
    async def perfil(self, ctx):
        """Mostra informações do perfil do usuário"""
        user_id = ctx.author.id
        
        # Verifica se usuário existe, se não cria
        if not self.db.user_exists(user_id):
            self.db.create_user(user_id, ctx.author.name, str(ctx.author.avatar))
        
        user_data = self.db.get_user(user_id)
        embed = CareerEmbed.create_profile_embed(user_data)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='carreira', aliases=['career'])
    async def carreira(self, ctx, user: discord.User = None):
        """Mostra a carreira do jogador"""
        
        if user is None:
            user = ctx.author
        
        user_id = user.id
        
        # Verifica se usuário existe
        if not self.db.user_exists(user_id):
            await ctx.send(f"❌ Usuário {user.name} ainda não tem carreira!")
            return
        
        user_data = self.db.get_user(user_id)
        career_data = self.db.get_career(user_id)
        trophies_data = self.db.get_trophies(user_id)
        
        embed = CareerEmbed.create_career_embed(user_data, career_data, trophies_data)
        await ctx.send(embed=embed)
    
    @commands.command(name='over')
    async def over(self, ctx):
        """Define o overall inicial do usuário"""
        user_id = ctx.author.id
        
        # Verifica se já usou
        if not self.db.user_exists(user_id):
            self.db.create_user(user_id, ctx.author.name, str(ctx.author.avatar))
        
        user_data = self.db.get_user(user_id)
        
        if user_data['over_used']:
            await ctx.send("❌ Você já utilizou o comando `!over`!")
            return
        
        # Pede confirmação
        embed = discord.Embed(
            title="⚠️ Confirmação",
            description="Tem certeza que quer girar o dado de Overall?\n\n"
                        "Isto sorteará um valor entre 50-70 que será seu Overall inicial.",
            color=discord.Color.yellow()
        )
        
        msg = await ctx.send(embed=embed)
        
        # Adiciona reações
        await msg.add_reaction('✅')
        await msg.add_reaction('❌')
        
        def check(reaction, user):
            return user == ctx.author and reaction.emoji in ['✅', '❌']
        
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
            
            if reaction.emoji == '✅':
                # Gira o dado
                import random
                from config import OVER_MIN, OVER_MAX
                
                overall = random.randint(OVER_MIN, OVER_MAX)
                self.db.set_overall(user_id, overall)
                self.db.mark_over_used(user_id)
                
                result_embed = discord.Embed(
                    title="🎲 Resultado",
                    description=f"Seu Overall Inicial: **{overall}**",
                    color=discord.Color.green()
                )
                
                await ctx.send(embed=result_embed)
            else:
                await ctx.send("❌ Comando cancelado.")
        
        except asyncio.TimeoutError:
            await ctx.send("⏰ Tempo expirado!")
    
    @commands.command(name='pot')
    async def pot(self, ctx):
        """Define o potencial máximo do usuário"""
        user_id = ctx.author.id
        
        if not self.db.user_exists(user_id):
            await ctx.send("❌ Você precisa usar `!over` antes!")
            return
        
        user_data = self.db.get_user(user_id)
        
        if user_data['pot_used']:
            await ctx.send("❌ Você já utilizou o comando `!pot`!")
            return
        
        if not user_data['overall']:
            await ctx.send("❌ Você precisa usar `!over` antes!")
            return
        
        # Pede confirmação
        embed = discord.Embed(
            title="⚠️ Confirmação",
            description="Tem certeza que quer girar o dado de Potencial?\n\n"
                        "Isto sorteará um valor entre 75-90 que será seu Potencial máximo.",
            color=discord.Color.yellow()
        )
        
        msg = await ctx.send(embed=embed)
        
        await msg.add_reaction('✅')
        await msg.add_reaction('❌')
        
        def check(reaction, user):
            return user == ctx.author and reaction.emoji in ['✅', '❌']
        
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=check)
            
            if reaction.emoji == '✅':
                import random
                from config import POTENTIAL_MIN, POTENTIAL_MAX
                
                potential = random.randint(POTENTIAL_MIN, POTENTIAL_MAX)
                self.db.set_potential(user_id, potential)
                self.db.mark_pot_used(user_id)
                
                result_embed = discord.Embed(
                    title="🎲 Resultado",
                    description=f"Seu Potencial Máximo: **{potential}**",
                    color=discord.Color.green()
                )
                
                await ctx.send(embed=result_embed)
            else:
                await ctx.send("❌ Comando cancelado.")
        
        except asyncio.TimeoutError:
            await ctx.send("⏰ Tempo expirado!")

async def setup(bot):
    await bot.add_cog(ProfileCog(bot))