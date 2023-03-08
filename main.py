import discord
from discord import app_commands
from riotwatcher import LolWatcher
from getChampionNameByID import get_champions_name
import random
import time
import os

# Version: 3.0.5 
# Author: KiraSenpai

class Unbroken(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.synced = False

    async def on_ready(self):
        await tree.sync(guild=discord.Object(id=821479008574242918))
        self.synced = True
        await client.change_presence(status=discord.Status.dnd, activity=discord.Game('Unbroken!'))
        print('Bot is now initialized... and online', f"latency: {round(client.latency * 1000)}ms")

client = Unbroken()
tree = app_commands.CommandTree(client)

# Application commands
@tree.command(name='ping', description='the ping the bot has with the server', guild=discord.Object(id=821479008574242918))
async def ping(ctx:discord.Interaction):
    """Shows the Latency between the server and the bot"""
    embed = discord.Embed(title=f"latency: {round(client.latency * 1000)}ms",
                          colour=discord.Colour.green())
    print('test')
    await ctx.response.send_message(embed=embed)

# League

@tree.command(name='profile', description='shows stats about your rank in this season', guild=discord.Object(id=821479008574242918))
async def profile(ctx:discord.Interaction, username:str):
    region = 'eun1'
    API = os.environ['LApi']
    lol_watcher = LolWatcher(API)
    me = lol_watcher.summoner.by_name(region, username)
    ranked_stats = lol_watcher.league.by_summoner(region, me['id'])
    lvl = me["summonerLevel"]
    code = me['profileIconId']
    id = me["id"]
    champs = lol_watcher.champion_mastery.by_summoner(region,id)
    championLevel = champs[0]['championLevel']
    championId = champs[0]['championId']
    championPoints = "{:,}".format(champs[0]['championPoints'])
    ranked_solo = None
    ranked_flex = None
    unranked = False
    both = False
    if ranked_stats == []:
        unranked = True
    else:
        for rank in ranked_stats:
            if rank['queueType'] == 'RANKED_SOLO_5x5':
                ranked_solo = rank
            if rank['queueType'] == 'RANKED_FLEX_SR':
                ranked_flex = rank
        if ranked_solo and ranked_flex:
            both = True
    if unranked:
        embed = discord.Embed(
            title=f"Level: {lvl}",
            description=f"Solo/Duo Wins: **Unranked** \n Flex Wins: **Unranked**",
            colour=discord.Colour.purple()
        )
        embed.add_field(
            name=f"Main's {get_champions_name(championId)}",
            value=f"Mastery Level: {championLevel} \n Points: {championPoints}",
            inline=True
        )
        embed.set_author(
            name=f"{me['name']}",
            icon_url=f"https://raw.communitydragon.org/latest/game/assets/ux/summonericons/profileicon{code}.png"
        )
        await ctx.response.send_message(embed=embed)
    elif both:
        #Solo duo 5x5 
        wins = ranked_solo['wins']
        losses = ranked_solo['losses']
        rank = ranked_solo['rank']
        lp = ranked_solo['leaguePoints']
        tier = ranked_solo['tier']
        #Flex 5x5
        tierf = ranked_flex["tier"]
        rankf = ranked_flex["rank"]
        winsf = ranked_flex["wins"]
        lossesf = ranked_flex["losses"]
        lpf = ranked_flex["leaguePoints"]
        embed = discord.Embed(
            title=f"Level: {lvl}",
            description=
            f"Solo/Duo Wins: **{wins}** Losses: **{losses}** Wins behind or ahead: **{wins - losses}** with **{round((wins/(wins+losses))*100)}%** Win rate. \n Flex Wins: **{winsf}** Losses: **{lossesf}** Wins behind or ahead: **{winsf - lossesf}** and with **{round((winsf/(winsf+lossesf))*100)}%** Win rate.",
            colour=discord.Colour.purple())
        embed.add_field(
            name="Solo/Duo",
            value=
            f"Tier: {tier} \n Rank: {rank} \n LP: {lp} \n Total Games: **{wins + losses}**",
            inline=True)
        embed.add_field(
            name="Flex",
            value=
            f"Tier: {tierf} \n Rank: {rankf} \n LP: {lpf} \n Total Games: **{winsf + lossesf}**",
            inline=True)
        embed.add_field(
            name=f"Main's {get_champions_name(championId)}",
            value=f"Mastery Level: {championLevel} \n Points: {championPoints}",
            inline=True
        )
        embed.set_author(
            name=f"{me['name']}",
            icon_url=
            f"https://raw.communitydragon.org/latest/game/assets/ux/summonericons/profileicon{code}.png"
        )
        rank_icon = str.lower(tier)
        embed.set_thumbnail(
            url=
            f"https://raw.communitydragon.org/latest/plugins/rcp-fe-lol-shared-components/global/default/{rank_icon}.png"
        )
        await ctx.response.send_message(embed=embed)
    elif ranked_solo:
        wins = ranked_solo['wins']
        losses = ranked_solo['losses']
        rank = ranked_solo['rank']
        lp = ranked_solo['leaguePoints']
        tier = ranked_solo['tier']
        embed = discord.Embed(
            title=f"Level: {lvl}",
            description=
            f"Solo/Duo Wins: **{wins}** Losses: **{losses}** Wins behind or ahead: **{wins - losses}** with **{round((wins/(wins+losses))*100)}%**  \n Flex Wins: No wins or losses",
            colour=discord.Colour.purple())
        embed.add_field(
            name="Solo/Duo",
            value=
            f"Tier: {tier} \n Rank: {rank} \n LP: {lp} \n Total Games: **{wins + losses}**",
            inline=True)
        embed.add_field(
            name=f"Main's {get_champions_name(championId)}",
            value=f"Mastery Level: {championLevel} \n Points: {championPoints}",
            inline=True
        )
        embed.set_author(
            name=f"{me['name']}",
            icon_url=
            f"https://raw.communitydragon.org/latest/game/assets/ux/summonericons/profileicon{code}.png"
        )
        rank_icon = str.lower(tier)
        embed.set_thumbnail(
            url=
            f"https://raw.communitydragon.org/latest/plugins/rcp-fe-lol-shared-components/global/default/{rank_icon}.png"
        )
        await ctx.response.send_message(embed=embed)
    elif ranked_flex:
        tierf = ranked_flex["tier"]
        rankf = ranked_flex["rank"]
        winsf = ranked_flex["wins"]
        lossesf = ranked_flex["losses"]
        lpf = ranked_flex["leaguePoints"]
        embed = discord.Embed(
            title=f"Level: {lvl}",
            description=
            f"Solo/Duo No Wins or Losses  \n Flex Wins: **{wins}** Losses: **{losses}** Wins behind or ahead: **{wins - losses}** with **{round((wins/(wins+losses))*100)}%** winrate",
            colour=discord.Colour.purple())
        embed.add_field(
            name="Flex",
            value=
            f"Tier: {tier} \n Rank: {rank} \n LP: {lp} \n Total Games: **{wins + losses}**",
            inline=True)
        embed.add_field(
            name=f"Main's {get_champions_name(championId)}",
            value=f"Mastery Level: {championLevel} \n Points: {championPoints}",
            inline=True
        )
        embed.set_author(
            name=f"{me['name']}",
            icon_url=
            f"https://raw.communitydragon.org/latest/game/assets/ux/summonericons/profileicon{code}.png"
        )
        rank_icon = str.lower(tier)
        embed.set_thumbnail(
            url=
            f"https://raw.communitydragon.org/latest/plugins/rcp-fe-lol-shared-components/global/default/{rank_icon}.png"
        )
        await ctx.response.send_message(embed=embed)

client.run(os.environ["DISCORD_TOKEN"])
