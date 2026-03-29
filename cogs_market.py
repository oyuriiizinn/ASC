import discord
from discord.ext import commands
from database import Database
from embeds import CareerEmbed

class MarketCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()
    
    @commands.command(name='proposta')
    async def proposta(self, ctx, user: discord.User = None):
        """Mostra a proposta de mercado do jogador"""
        
        if user is None:
            user = ctx.author
        
        user_id = user.id
        
        if not self.db.user_exists(user_id):
            await ctx.send(f"❌ Usuário {user.name} ainda não tem carreira!")
            return
        
        user_data = self.db.get_user(user_id)
        career_data = self.db.get_career(user_id)
        
        if not user_data['overall']:
            await ctx.send(f"❌ {user.name} ainda não definiu seu overall!")
            return
        
        embed = CareerEmbed.create_market_embed(user_data, career_data)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(MarketCog(bot))