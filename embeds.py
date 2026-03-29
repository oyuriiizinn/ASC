from discord import Embed, Color
from datetime import datetime, timedelta

class CareerEmbed:
    """Classe para gerar embeds de carreira"""
    
    @staticmethod
    def create_career_embed(user_data, career_data, trophies_data):
        """Cria embed principal de carreira"""
        
        embed = Embed(
            title="",
            description="",
            color=Color.gold()
        )
        
        position = career_data['position'] if career_data['position'] else 'Indefinido'
        
        # Header
        embed.add_field(
            name="⠀︵⠀🚀 𝙰𝚝𝚕𝚊𝚗𝚝𝚊 𝙲𝚑𝚊𝚖𝚙𝚒𝚘𝚗𝚜 𝚂𝚒𝚖𝚞𝚕𝚊𝚝𝚘𝚛",
            value=f"⠀◌Ⳋ𝅄 ՚ 谷﹒`📍` {position}\n",
            inline=False
        )
        
        # Dados de Carreira
        embed.add_field(
            name="‧˚꒰`📊`꒱༘‧— 𝘿𝙖𝙙𝙤𝙨 𝙙𝙚 𝘾𝙖𝙧𝙧𝙚𝙞𝙧𝙖:",
            value=(
                f"﹕𐔌・`⚽`〃・꒱ Gols: {career_data['goals']}\n"
                f"﹕𐔌・`👟`〃・꒱ Assistências: {career_data['assists']}\n"
                f"﹕𐔌・`✅`〃・꒱ Vitórias: {career_data['wins']}\n"
                f"﹕𐔌・`🧩`〃・꒱ Empates: {career_data['draws']}\n"
                f"﹕𐔌・`❌`〃・꒱ Derrotas: {career_data['losses']}\n"
            ),
            inline=False
        )
        
        # Troféus Brasil
        embed.add_field(
            name="⠀︵⠀🇧🇷 𝐁𝐫𝐚𝐬𝐢𝐥!⠀◌Ⳋ𝅄",
            value=(
                f"﹕𐔌・<:asc_brasileirao:1473743887511326730>〃・꒱ Brasileirão: {trophies_data['brasileirao']}\n"
                f"﹕𐔌・<:asc_cdb:1473744253841576028>〃・꒱ Copa do Brasil: {trophies_data['copa_brasil']}\n"
                f"﹕𐔌・<:asc_supercopabr:1473744503834673263>〃・꒱ Supercopa do Brasil: {trophies_data['supercopa_brasil']}\n"
            ),
            inline=False
        )
        
        # Troféus Argentina
        embed.add_field(
            name="⠀︵⠀🇦🇷 𝐀𝐫𝐠𝐞𝐧𝐭𝐢𝐧𝐚!⠀◌Ⳋ𝅄",
            value=(
                f"﹕𐔌・<:asc_ligaprofessional:1473745536271253659>〃・꒱ Liga Profesional: {trophies_data['liga_profesional']}\n"
                f"﹕𐔌・<:asc_copaargentina:1473745896134021372>〃・꒱ Copa da Argentina: {trophies_data['copa_argentina']}\n"
                f"﹕𐔌・<:asc_supercopaarg:1473746180469948710>〃・꒱ Supercopa Arg: {trophies_data['supercopa_argentina']}\n"
            ),
            inline=False
        )
        
        # Troféus Uruguay
        embed.add_field(
            name="⠀︵⠀🇺🇾 𝐔𝐫𝐮𝐠𝐮𝐚𝐢!⠀◌Ⳋ𝅄",
            value=(
                f"﹕𐔌・<:asc_ligaauf:1473745678072283288>〃・꒱ Liga AUF: {trophies_data['liga_auf']}\n"
                f"﹕𐔌・<:asc_copaauf:1473746032725594290>〃・꒱ Copa AUF: {trophies_data['copa_auf']}\n"
                f"﹕𐔌・<:asc_supercopauru:1473746273499742209>〃・꒱ Supercopa Uruguay: {trophies_data['supercopa_uruguay']}\n"
            ),
            inline=False
        )
        
        # Troféus Continentais
        embed.add_field(
            name="⠀︵⠀🌎 𝐂𝐨𝐧𝐭𝐢𝐧𝐞𝐧𝐭𝐚𝐢𝐬 & 𝐈𝐧𝐭𝐞𝐫𝐜𝐨𝐧𝐭𝐢𝐧𝐞𝐧𝐭𝐚𝐢𝐬!⠀◌Ⳋ𝅄",
            value=(
                f"﹕𐔌・<:asc_libertadores:1473744310548693116>〃・꒱ Libertadores: {trophies_data['libertadores']}\n"
                f"﹕𐔌・<:asc_sudamericana:1473744366047854687>〃・꒱ Sudamericana: {trophies_data['sudamericana']}\n"
                f"﹕𐔌・<:asc_recopa:1473744545639305247>〃・꒱ Recopa: {trophies_data['recopa']}\n"
                f"﹕𐔌・<:asc_intercontinental:1473744662434156799>〃・꒱ Intercontinental: {trophies_data['intercontinental']}\n"
                f"﹕𐔌・<:asc_mundial:1473744778553458881>〃・꒱ Copa do Mundo de Clubes: {trophies_data['mundial_clubes']}\n"
                f"﹕𐔌・<:asc_copadomundo:1473745099610525850>〃・꒱ Copa do Mundo: {trophies_data['copa_mundo']}\n"
            ),
            inline=False
        )
        
        # OVR
        overall = user_data['overall'] if user_data['overall'] else 'Indefinido'
        embed.add_field(
            name="‧˚꒰`⭐`꒱༘‧— 𝘿𝙖𝙙𝙤𝙨 𝙙𝙚 𝙾𝚅𝚁:",
            value=f"﹕𐔌・`🌺`〃・꒱ Overall Atual: {overall}",
            inline=False
        )
        
        return embed
    
    @staticmethod
    def create_profile_embed(user_data):
        """Cria embed de perfil"""
        
        embed = Embed(
            title=f"👤 Perfil - {user_data['username']}",
            color=Color.blue()
        )
        
        # Calcula tempo no servidor
        join_date = datetime.fromisoformat(user_data['server_join_date'])
        time_on_server = datetime.now() - join_date
        days = time_on_server.days
        
        level = user_data['level']
        xp = user_data['xp']
        
        embed.add_field(
            name="📊 Informações",
            value=(
                f"**Nick:** {user_data['username']}\n"
                f"**Level:** {level}/100\n"
                f"**XP:** {xp}\n"
                f"**Tempo no Servidor:** {days} dias\n"
            ),
            inline=False
        )
        
        if user_data['avatar_url']:
            embed.set_thumbnail(url=user_data['avatar_url'])
        
        return embed
    
    @staticmethod
    def create_market_embed(user_data, career_data):
        """Cria embed de proposta de mercado"""
        
        overall = user_data['overall'] if user_data['overall'] else 0
        potential = user_data['potential'] if user_data['potential'] else 0
        
        # Calcula valor de mercado baseado em overall e stats
        base_value = overall * 1_000_000  # Base: 1M por ponto de overall
        
        # Bonificadores
        goals_bonus = career_data['goals'] * 500_000
        assists_bonus = career_data['assists'] * 300_000
        wins_bonus = career_data['wins'] * 200_000
        
        total_value = base_value + goals_bonus + assists_bonus + wins_bonus
        
        embed = Embed(
            title="💰 Proposta de Mercado",
            color=Color.green()
        )
        
        embed.add_field(
            name="Informações do Jogador",
            value=(
                f"**Nick:** {user_data['username']}\n"
                f"**Overall:** {overall}\n"
                f"**Potencial:** {potential}\n"
            ),
            inline=False
        )
        
        embed.add_field(
            name="Cálculo de Valor",
            value=(
                f"Base (OVR): R$ {base_value:,.0f}\n"
                f"Gols: +R$ {goals_bonus:,.0f}\n"
                f"Assistências: +R$ {assists_bonus:,.0f}\n"
                f"Vitórias: +R$ {wins_bonus:,.0f}\n"
                f"**Total: R$ {total_value:,.0f}**\n"
            ),
            inline=False
        )
        
        return embed

class TrainingEmbed:
    """Classe para embeds de treino"""
    
    @staticmethod
    def create_training_result_embed(user_data, event_data, over_before, over_after, consecutive=0):
        """Cria embed de resultado de treino"""
        
        color = Color.gold()
        if event_data['rarity'] == 'common':
            color = Color.greyple()
        elif event_data['rarity'] == 'uncommon':
            color = Color.green()
        elif event_data['rarity'] == 'rare':
            color = Color.blue()
        elif event_data['rarity'] == 'epic':
            color = Color.purple()
        
        embed = Embed(
            title=f"🏋️ Resultado do Treino - {event_data['name']}",
            color=color
        )
        
        embed.add_field(
            name="📊 Mudanças",
            value=(
                f"**Overall Antes:** {over_before}\n"
                f"**Overall Depois:** {over_after}\n"
                f"**Diferença:** {'+' if over_after > over_before else ''}{over_after - over_before}\n"
            ),
            inline=False
        )
        
        if event_data.get('injury'):
            embed.add_field(
                name="🩹 Lesão",
                value=f"Você se lesionou! {event_data['games_out']} jogos sem jogar.",
                inline=False
            )
        
        if consecutive > 0:
            embed.add_field(
                name="✨ Treinos Bons Consecutivos",
                value=f"{consecutive}/6 para +2 de overall adicional!",
                inline=False
            )
        
        return embed