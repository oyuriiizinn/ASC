import discord
from discord.ext import commands
from database import Database

class EditCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = Database()
    
    def _get_trophy_field(self, trophy_name):
        """Mapeia nome do comando para campo do banco"""
        trophy_map = {
            'br': 'brasileirao',
            'cdb': 'copa_brasil',
            'sbr': 'supercopa_brasil',
            'arg': 'liga_profesional',
            'cda': 'copa_argentina',
            'sarg': 'supercopa_argentina',
            'auf': 'liga_auf',
            'cdu': 'copa_auf',
            'suru': 'supercopa_uruguay',
            'lib': 'libertadores',
            'sud': 'sudamericana',
            'rec': 'recopa',
            'intercontinental': 'intercontinental',
            'mundial': 'mundial_clubes',
            'cdm': 'copa_mundo',
        }
        return trophy_map.get(trophy_name)
    
    # Comandos de carreira
    @commands.command(name='alterar-posicao')
    async def alterar_posicao(self, ctx, *, posicao):
        """Altera a posição do jogador"""
        user_id = ctx.author.id
        
        if not self.db.user_exists(user_id):
            await ctx.send("❌ Você ainda não tem carreira!")
            return
        
        self.db.update_career(user_id, position=posicao)
        await ctx.send(f"✅ Posição alterada para: **{posicao}**")
    
    @commands.command(name='alterar-gols')
    async def alterar_gols(self, ctx, valor: int):
        """Altera gols do jogador"""
        user_id = ctx.author.id
        
        if not self.db.user_exists(user_id):
            await ctx.send("❌ Você ainda não tem carreira!")
            return
        
        self.db.update_career(user_id, goals=valor)
        await ctx.send(f"✅ Gols alterados para: **{valor}**")
    
    @commands.command(name='alterar-ass')
    async def alterar_ass(self, ctx, valor: int):
        """Altera assistências do jogador"""
        user_id = ctx.author.id
        
        if not self.db.user_exists(user_id):
            await ctx.send("❌ Você ainda não tem carreira!")
            return
        
        self.db.update_career(user_id, assists=valor)
        await ctx.send(f"✅ Assistências alteradas para: **{valor}**")
    
    @commands.command(name='alterar-vit')
    async def alterar_vit(self, ctx, valor: int):
        """Altera vitórias do jogador"""
        user_id = ctx.author.id
        
        if not self.db.user_exists(user_id):
            await ctx.send("❌ Você ainda não tem carreira!")
            return
        
        self.db.update_career(user_id, wins=valor)
        await ctx.send(f"✅ Vitórias alteradas para: **{valor}**")
    
    @commands.command(name='alterar-der')
    async def alterar_der(self, ctx, valor: int):
        """Altera derrotas do jogador"""
        user_id = ctx.author.id
        
        if not self.db.user_exists(user_id):
            await ctx.send("❌ Você ainda não tem carreira!")
            return
        
        self.db.update_career(user_id, losses=valor)
        await ctx.send(f"✅ Derrotas alteradas para: **{valor}**")
    
    @commands.command(name='alterar-emp')
    async def alterar_emp(self, ctx, valor: int):
        """Altera empates do jogador"""
        user_id = ctx.author.id
        
        if not self.db.user_exists(user_id):
            await ctx.send("❌ Você ainda não tem carreira!")
            return
        
        self.db.update_career(user_id, draws=valor)
        await ctx.send(f"✅ Empates alterados para: **{valor}**")
    
    # Comandos de troféus
    @commands.command(name='alterar-br')
    async def alterar_br(self, ctx, valor: int):
        """Altera Brasileirão"""
        user_id = ctx.author.id
        if not self.db.user_exists(user_id):
            await ctx.send("❌ Você ainda não tem carreira!")
            return
        self.db.update_trophy(user_id, 'brasileirao', valor)
        await ctx.send(f"✅ Brasileirão alterado para: **{valor}**")
    
    @commands.command(name='alterar-cdb')
    async def alterar_cdb(self, ctx, valor: int):
        """Altera Copa do Brasil"""
        user_id = ctx.author.id
        if not self.db.user_exists(user_id):
            await ctx.send("❌ Você ainda não tem carreira!")
            return
        self.db.update_trophy(user_id, 'copa_brasil', valor)
        await ctx.send(f"✅ Copa do Brasil alterada para: **{valor}**")
    
    @commands.command(name='alterar-sbr')
    async def alterar_sbr(self, ctx, valor: int):
        """Altera Supercopa do Brasil"""
        user_id = ctx.author.id
        if not self.db.user_exists(user_id):
            await ctx.send("❌ Você ainda não tem carreira!")
            return
        self.db.update_trophy(user_id, 'supercopa_brasil', valor)
        await ctx.send(f"✅ Supercopa do Brasil alterada para: **{valor}**")
    
    @commands.command(name='alterar-arg')
    async def alterar_arg(self, ctx, valor: int):
        """Altera Liga Profesional"""
        user_id = ctx.author.id
        if not self.db.user_exists(user_id):
            await ctx.send("❌ Você ainda não tem carreira!")
            return
        self.db.update_trophy(user_id, 'liga_profesional', valor)
        await ctx.send(f"✅ Liga Profesional alterada para: **{valor}**")
    
    @commands.command(name='alterar-cda')
    async def alterar_cda(self, ctx, valor: int):
        """Altera Copa da Argentina"""
        user_id = ctx.author.id
        if not self.db.user_exists(user_id):
            await ctx.send("❌ Você ainda não tem carreira!")
            return
        self.db.update_trophy(user_id, 'copa_argentina', valor)
        await ctx.send(f"✅ Copa da Argentina alterada para: **{valor}**")
    
    @commands.command(name='alterar-sarg')
    async def alterar_sarg(self, ctx, valor: int):
        """Altera Supercopa Argentina"""
        user_id = ctx.author.id
        if not self.db.user_exists(user_id):
            await ctx.send("❌ Você ainda não tem carreira!")
            return
        self.db.update_trophy(user_id, 'supercopa_argentina', valor)
        await ctx.send(f"✅ Supercopa Argentina alterada para: **{valor}**")
    
    @commands.command(name='alterar-auf')
    async def alterar_auf(self, ctx, valor: int):
        """Altera Liga AUF"""
        user_id = ctx.author.id
        if not self.db.user_exists(user_id):
            await ctx.send("❌ Você ainda não tem carreira!")
            return
        self.db.update_trophy(user_id, 'liga_auf', valor)
        await ctx.send(f"✅ Liga AUF alterada para: **{valor}**")
    
    @commands.command(name='alterar-cdu')
    async def alterar_cdu(self, ctx, valor: int):
        """Altera Copa AUF"""
        user_id = ctx.author.id
        if not self.db.user_exists(user_id):
            await ctx.send("❌ Você ainda não tem carreira!")
            return
        self.db.update_trophy(user_id, 'copa_auf', valor)
        await ctx.send(f"✅ Copa AUF alterada para: **{valor}**")
    
    @commands.command(name='alterar-suru')
    async def alterar_suru(self, ctx, valor: int):
        """Altera Supercopa Uruguay"""
        user_id = ctx.author.id
        if not self.db.user_exists(user_id):
            await ctx.send("❌ Você ainda não tem carreira!")
            return
        self.db.update_trophy(user_id, 'supercopa_uruguay', valor)
        await ctx.send(f"✅ Supercopa Uruguay alterada para: **{valor}**")
    
    @commands.command(name='alterar-lib')
    async def alterar_lib(self, ctx, valor: int):
        """Altera Libertadores"""
        user_id = ctx.author.id
        if not self.db.user_exists(user_id):
            await ctx.send("❌ Você ainda não tem carreira!")
            return
        self.db.update_trophy(user_id, 'libertadores', valor)
        await ctx.send(f"✅ Libertadores alterada para: **{valor}**")
    
    @commands.command(name='alterar-sud')
    async def alterar_sud(self, ctx, valor: int):
        """Altera Sudamericana"""
        user_id = ctx.author.id
        if not self.db.user_exists(user_id):
            await ctx.send("❌ Você ainda não tem carreira!")
            return
        self.db.update_trophy(user_id, 'sudamericana', valor)
        await ctx.send(f"✅ Sudamericana alterada para: **{valor}**")
    
    @commands.command(name='alterar-rec')
    async def alterar_rec(self, ctx, valor: int):
        """Altera Recopa"""
        user_id = ctx.author.id
        if not self.db.user_exists(user_id):
            await ctx.send("❌ Você ainda não tem carreira!")
            return
        self.db.update_trophy(user_id, 'recopa', valor)
        await ctx.send(f"✅ Recopa alterada para: **{valor}**")
    
    @commands.command(name='alterar-intercontinental')
    async def alterar_intercontinental(self, ctx, valor: int):
        """Altera Intercontinental"""
        user_id = ctx.author.id
        if not self.db.user_exists(user_id):
            await ctx.send("❌ Você ainda não tem carreira!")
            return
        self.db.update_trophy(user_id, 'intercontinental', valor)
        await ctx.send(f"✅ Intercontinental alterado para: **{valor}**")
    
    @commands.command(name='alterar-mundial')
    async def alterar_mundial(self, ctx, valor: int):
        """Altera Copa do Mundo de Clubes"""
        user_id = ctx.author.id
        if not self.db.user_exists(user_id):
            await ctx.send("❌ Você ainda não tem carreira!")
            return
        self.db.update_trophy(user_id, 'mundial_clubes', valor)
        await ctx.send(f"✅ Copa do Mundo de Clubes alterada para: **{valor}**")
    
    @commands.command(name='alterar-cdm')
    async def alterar_cdm(self, ctx, valor: int):
        """Altera Copa do Mundo"""
        user_id = ctx.author.id
        if not self.db.user_exists(user_id):
            await ctx.send("❌ Você ainda não tem carreira!")
            return
        self.db.update_trophy(user_id, 'copa_mundo', valor)
        await ctx.send(f"✅ Copa do Mundo alterada para: **{valor}**")

async def setup(bot):
    await bot.add_cog(EditCog(bot))