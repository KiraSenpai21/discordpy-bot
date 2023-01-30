import discord
from discord import app_commands
from riotwatcher import LolWatcher
from getChampionNameByID import get_champions_name
import random
import time
import os


class Unbroken(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.synced = False

    async def on_ready(self):
        await tree.sync(guild=discord.Object(id=821479008574242918))
        self.synced = True
        await client.change_presence(status=discord.Status.dnd, activity=discord.Game('Unbroken!'))
        print('Bot is now initialized... and online', f"latency: {round(client.latency * 1000)}ms")
        # for filename in os.listdir("./cogs"):
        #     if filename.endswith(".py") and filename != "__init__.py":
        #         client.load_extension(f'cogs.{filename[:-3]}')
                

client = Unbroken()
tree = app_commands.CommandTree(client)

# Application commands
@tree.command(name='ping', description='the ping the bot has with the server', guild=discord.Object(id=821479008574242918))
async def ping(ctx:discord.Interaction):
    """Shows the Latency between the server and the bot"""
    embed = discord.Embed(title=f"latency: {round(client.latency * 1000)}ms",
                          colour=discord.Colour.green())
    await ctx.response.send_message(embed=embed)

# League

@tree.command(name='profile', description='shows stats about your rank in this season', guild=discord.Object(id=821479008574242918))
async def profile(ctx:discord.Interaction, username:str):
      prefix = '$'
      version = '12.8'
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
      if ranked_stats[0]["queueType"] == 'RANKED_TFT_PAIRS':
        if len(ranked_stats) == 3:
          if ranked_stats[1]["queueType"] == 'RANKED_FLEX_SR':
              flexed = ranked_stats[1]  
              ranked = ranked_stats[2]
          else:
              flexed = ranked_stats[2]
              ranked = ranked_stats[1]
        elif len(ranked_stats) == 2:
          if ranked_stats[1]["queueType"] == 'RANKED_SOLO_5x5':
              ranked = ranked_stats[1]
              flexed = []
          else:
              flexed = ranked_stats[1]
              ranked = []
      else:
        if len(ranked_stats) == 2:
          if ranked_stats[0]["queueType"] == 'RANKED_FLEX_SR':
              flexed = ranked_stats[0]  
              ranked = ranked_stats[1]
          else:
              flexed = ranked_stats[1]
              ranked = ranked_stats[0]
        elif len(ranked_stats) == 1:
          if ranked_stats[0]["queueType"] == 'RANKED_SOLO_5x5':
              ranked = ranked_stats[0]
              flexed = []
          else:
              flexed = ranked_stats[0]
              ranked = []
#KATHOLOU RANKED
      if len(ranked_stats) == 0:
          embed = discord.Embed(
              title=f"Level: {lvl}",
              description=
              f"Solo/Duo Wins: Unranked \n Flex Wins: Unranked",
              colour=discord.Colour.green())
          embed.add_field(name="Solo/Duo",
                          value=f"Unranked",
                          inline=True)
          embed.add_field(name="Flex",
                          value=f"Unranked",
                          inline=True)
          embed.set_author(
              name=f"{me['name']}",
              icon_url=
              f"https://raw.communitydragon.org/latest/game/assets/ux/summonericons/profileicon{code}.png"
          )
          await ctx.response.send_message(embed=embed)
#MONO SOLO/DUO
      elif flexed == []:
          tier = ranked["tier"]
          rank = ranked["rank"]
          wins = ranked["wins"]
          losses = ranked["losses"]
          lp = ranked["leaguePoints"]
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
#MONO FLEX
      elif ranked == []:
          tier = flexed["tier"]
          rank = flexed["rank"]
          wins = flexed["wins"]
          losses = flexed["losses"]
          lp = flexed["leaguePoints"]
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
