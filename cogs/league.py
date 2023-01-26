import discord
from discord.ext import commands
from riotwatcher import LolWatcher
# from replit import db
from getChampionNameByID import get_champions_name
import random
import time
import os

prefix = '$'
version = '12.8'
region = 'eun1'

########### League of legends  ##################

API = os.environ['LApi']


class league(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(pass_context=True, aliases=['prof', 'stats'])
  async def profile(self, ctx, *, username):
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
          await ctx.send(embed=embed)
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
              f"Solo/Duo Wins: **{wins}** Losses: **{losses}** Wins behind or ahead: **{wins - losses}**  \n Flex Wins: No wins or losses",
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
          await ctx.send(embed=embed)
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
              f"Solo/Duo No Wins or Losses  \n Flex Wins: **{wins}** Losses: **{losses}** Wins behind or ahead: **{wins - losses}**",
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
          await ctx.send(embed=embed)

#KAI TA DIO
      elif not ranked == [] and not flexed == [] and not ranked_stats[0]["queueType"] == 'RANKED_TFT_PAIRS':
          tier = ranked["tier"]
          rank = ranked["rank"]
          wins = ranked["wins"]
          losses = ranked["losses"]
          lp = ranked["leaguePoints"]
          tierf = flexed["tier"]
          rankf = flexed["rank"]
          winsf = flexed["wins"]
          lossesf = flexed["losses"]
          lpf = flexed["leaguePoints"]
          embed = discord.Embed(
              title=f"Level: {lvl}",
              description=
              f"Solo/Duo Wins: **{wins}** Losses: **{losses}** Wins behind or ahead: **{wins - losses}**  \n Flex Wins: **{winsf}** Losses: **{lossesf}** Wins behind or ahead: **{winsf - lossesf}**",
              colour=discord.Colour.purple())
          embed.add_field(
              name="Solo/Duo",
              value=
              f"Tier: {tier} \n Rank: {rank} \n LP: {lp} \n Total Games: **{wins + losses}**",
              inline=True)
          embed.add_field(
              name="Flex",
              value=
              f"Tier: {tierf} \n Rank: {rankf} \n LP: {lpf} \n Total Games: {winsf + lossesf}",
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
          await ctx.send(embed=embed)
      else:
        tier = ranked["tier"]
        rank = ranked["rank"]
        wins = ranked["wins"]
        losses = ranked["losses"]
        lp = ranked["leaguePoints"]
        tierf = flexed["tier"]
        rankf = flexed["rank"]
        winsf = flexed["wins"]
        lossesf = flexed["losses"]
        lpf = flexed["leaguePoints"]
        embed = discord.Embed(
            title=f"Level: {lvl}",
            description=
            f"Solo/Duo Wins: **{wins}** Losses: **{losses}** Wins behind or ahead: **{wins - losses}**  \n Flex Wins: **{winsf}** Losses: **{lossesf}** Wins behind or ahead: **{winsf - lossesf}**",
            colour=discord.Colour.purple())
        embed.add_field(
            name="Solo/Duo",
            value=
            f"Tier: {tier} \n Rank: {rank} \n LP: {lp} \n Total Games: **{wins + losses}**",
            inline=True)
        embed.add_field(
            name="Flex",
            value=
            f"Tier: {tierf} \n Rank: {rankf} \n LP: {lpf} \n Total Games: {winsf + lossesf}",
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
        await ctx.send(embed=embed)




        
##################################################

  @commands.command()
  @commands.has_permissions(administrator=True)
  async def clear_database(self, ctx):
      keys = db.keys()
      count = 0
      for key in keys:
          del db[key]
          count += 1
      if count >= 1:
          embed = discord.Embed(
              title='Successful',
              description=f'Database cleared {count} items',
              colour=discord.Colour.green())
          await ctx.send(embed=embed)
      elif count == 0:
          embed = discord.Embed(
              title='No Items to be deleted',
              description=f'Database cleared {count} items',
              colour=discord.Colour.red())
          await ctx.send(embed=embed)

  @commands.command()
  @commands.has_permissions(administrator=True)
  async def database_keys(self, ctx):
      keys = db.keys()
      keys = keys
      embed = discord.Embed(
          title='List of all the Users in The Database',
          description=f'{keys}',
          colour=discord.Colour.purple())
      await ctx.send(embed=embed)

#### ME COMMAND #####

  @commands.command()
  async def me(self, ctx):
      username = db[f"{ctx.author.id}"]
      lol_watcher = LolWatcher(API)
      me = lol_watcher.summoner.by_name(region, username)
      id = me["id"]
      champs = lol_watcher.champion_mastery.by_summoner(region,id)
      championLevel = champs[0]['championLevel']
      championId = champs[0]['championId']
      championPoints = "{:,}".format(champs[0]['championPoints'])
      lvl = me["summonerLevel"]
      ranked_stats = lol_watcher.league.by_summoner(
          region, me['id'])
      code = me['profileIconId']

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
              colour=discord.Colour.purple())
          embed.add_field(name="Solo/Duo",
                          value=f"Unranked",
                          inline=True)
          embed.add_field(name="Flex",
                          value=f"Unranked",
                          inline=True)
          embed.add_field(
              name=f"Main's {get_champions_name(championId)}",
              value=f"Mastery Level: {championLevel} \n Points: {championPoints}",
              inline=True
          )
          embed.set_author(name=f"{me['name']}",icon_url=f"https://raw.communitydragon.org/latest/game/assets/ux/summonericons/profileicon{code}.png")
          await ctx.send(embed=embed)
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
              f"Solo/Duo Wins: **{wins}** Losses: **{losses}** Wins behind or ahead: **{wins - losses}**  \n Flex Wins: No wins or losses",
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
          embed.set_thumbnail(url=f"https://raw.communitydragon.org/latest/plugins/rcp-fe-lol-shared-components/global/default/{rank_icon}.png")
          await ctx.send(embed=embed)
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
              f"Solo/Duo No Wins or Losses  \n Flex Wins: **{wins}** Losses: **{losses}** Wins behind or ahead: **{wins - losses}**",
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
          await ctx.send(embed=embed)

#KAI TA DIO
      elif not ranked == [] and not flexed == [] and not ranked_stats[0]["queueType"] == 'RANKED_TFT_PAIRS':
          tier = ranked["tier"]
          rank = ranked["rank"]
          wins = ranked["wins"]
          losses = ranked["losses"]
          lp = ranked["leaguePoints"]
          tierf = flexed["tier"]
          rankf = flexed["rank"]
          winsf = flexed["wins"]
          lossesf = flexed["losses"]
          lpf = flexed["leaguePoints"]
          embed = discord.Embed(
              title=f"Level: {lvl}",
              description=
              f"Solo/Duo Wins: **{wins}** Losses: **{losses}** Wins behind or ahead: **{wins - losses}**  \n Flex Wins: **{winsf}** Losses: **{lossesf}** Wins behind or ahead: **{winsf - lossesf}**",
              colour=discord.Colour.purple())
          embed.add_field(
              name="Solo/Duo",
              value=
              f"Tier: {tier} \n Rank: {rank} \n LP: {lp} \n Total Games: **{wins + losses}**",
              inline=True)
          embed.add_field(
              name="Flex",
              value=
              f"Tier: {tierf} \n Rank: {rankf} \n LP: {lpf} \n Total Games: {winsf + lossesf}",
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
          await ctx.send(embed=embed)
      else:
        tier = ranked["tier"]
        rank = ranked["rank"]
        wins = ranked["wins"]
        losses = ranked["losses"]
        lp = ranked["leaguePoints"]
        tierf = flexed["tier"]
        rankf = flexed["rank"]
        winsf = flexed["wins"]
        lossesf = flexed["losses"]
        lpf = flexed["leaguePoints"]
        embed = discord.Embed(
            title=f"Level: {lvl}",
            description=
            f"Solo/Duo Wins: **{wins}** Losses: **{losses}** Wins behind or ahead: **{wins - losses}**  \n Flex Wins: **{winsf}** Losses: **{lossesf}** Wins behind or ahead: **{winsf - lossesf}**",
            colour=discord.Colour.purple())
        embed.add_field(
            name="Solo/Duo",
            value=
            f"Tier: {tier} \n Rank: {rank} \n LP: {lp} \n Total Games: **{wins + losses}**",
            inline=True)
        embed.add_field(
            name="Flex",
            value=
            f"Tier: {tierf} \n Rank: {rankf} \n LP: {lpf} \n Total Games: {winsf + lossesf}",
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
        await ctx.send(embed=embed)

#####################################################

  @commands.command(pass_context=True, aliases=['freg', 'forcereg'])
  @commands.has_permissions(administrator=True)
  async def force_register(self, ctx, id, *, username:str):
    db[id] = f"{username}"
    embed = discord.Embed(
        title='Registered',
        description=f'User with id: {id} has been registered as {username}',
        colour=discord.Colour.blue())
    await ctx.send(embed=embed)

#### REGISTER COMMAND ####

  @commands.command(pass_context=True, aliases=['reg', 'setup'])
  async def register(self, ctx, *, username: str):
      guild = ctx.guild
      lol_watcher = LolWatcher(API)
      my_region = 'eun1'
      me = lol_watcher.summoner.by_name(my_region, f"{username}")
      ranked_stats = lol_watcher.league.by_summoner(my_region, me['id'])
      code = me['profileIconId']
      random_nm = random.randrange(1, 30)
      embed = discord.Embed(
          title='Verification',
          description='You have to switch to the icon that is shown to verify your account, you have 30 seconds',
          colour=discord.Colour.blue())
      embed.set_thumbnail(
          url=f"https://raw.communitydragon.org/latest/game/assets/ux/summonericons/profileicon{random_nm}.png"
      )
      await ctx.send(embed=embed)
      timeout = time.time() + 30
      failed = None
      while code != random_nm:
          me = lol_watcher.summoner.by_name(my_region, username)
          code = me['profileIconId']
          if time.time() > timeout:
              embed = discord.Embed(
                  title='Verification Failed',
                  description='You took too long to change your profile icon',
                  colour=discord.Colour.red())
              await ctx.send(embed=embed)
              failed = True
              break
      if code == random_nm:
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

            
          if len(ranked_stats) == 0:
              guild = ctx.guild
              rank_role = discord.utils.get(guild.roles, name="UNRANKED")
              await ctx.author.add_roles(rank_role)
              rank_role = discord.utils.get(guild.roles, name="EUNE")
              await ctx.author.add_roles(rank_role)
          elif flexed == []:
              rank = ranked["tier"]
              rank_role = discord.utils.get(guild.roles, name=f"{rank}")
              await ctx.author.add_roles(rank_role)
              rank_role = discord.utils.get(guild.roles, name="EUNE")
              await ctx.author.add_roles(rank_role)
          else:
              rank = ranked["tier"]
              rank_role = discord.utils.get(guild.roles,name=f"{rank}")
              await ctx.author.add_roles(rank_role)
              rank_role = discord.utils.get(guild.roles, name="EUNE")
              await ctx.author.add_roles(rank_role)
          embed = discord.Embed(
              title='Verification Complete!',
              description=f'You can now use the Command **{prefix}me** and have now got the roles of your accounts rank',
              colour=discord.Colour.green())
          await ctx.send(embed=embed)
          db[ctx.author.id] = f"{username}"
      elif code != random_nm and failed == False:
          embed = discord.Embed(
              title='Verification Failed',
              description='No changes were made to your profile icon',
              colour=discord.Colour.red())
          await ctx.send(embed=embed)

  @commands.command(pass_context=True)
  async def delete_acc(self, ctx, *, username: str):
      del db[f"{ctx.author.id}"]
      embed = discord.Embed(
          title=f'Deleted {username} Account Binded to {ctx.author}',
          description=f'The league account binded to your discord is now deleted',
          colour=discord.Colour.green())
      await ctx.send(embed=embed)

  @commands.command(pass_context=True, aliases=['rankup', 'rankupdate'])
  async def update(self, ctx):
    username = db[f"{ctx.author.id}"]
    guild = ctx.guild
    lol_watcher = LolWatcher(API)
    me = lol_watcher.summoner.by_name(region, f"{username}")
    ranked_stats = lol_watcher.league.by_summoner(region, me['id'])

    ranks = ['UNRANKED', 'IRON', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'DIAMOND', 'MASTER', 'GRAND MASTER', 'CHALLENGER']
    
    if len(ranked_stats) == 2:
      if ranked_stats[0]["queueType"] == 'RANKED_FLEX_SR':
          ranked = ranked_stats[1]
          flexed = ranked_stats[0]
      else:
          ranked = ranked_stats[0]
          flexed = ranked_stats[1]
    elif len(ranked_stats) == 1:
      if ranked_stats[0]["queueType"] == 'RANKED_SOLO_5x5':
          ranked = ranked_stats[0]
          flexed = []
      else:
          ranked = []
        
    if len(ranked_stats) == 0:
      guild = ctx.guild
      rank_role = discord.utils.get(guild.roles, name="UNRANKED")
      await ctx.author.add_roles(rank_role)
      rank_role = discord.utils.get(guild.roles, name="EUNE")
      await ctx.author.add_roles(rank_role)
    elif flexed == []:
      rank = ranked["tier"]
      rank_role = discord.utils.get(guild.roles, name=f"{rank}")
      for Tier in ranks:
        if Tier in ctx.author.roles:
          ctx.author.remove_roles(guild.roles, name=f'{Tier}')
      await ctx.author.add_roles(rank_role)
      rank_role = discord.utils.get(guild.roles, name="EUNE")
      await ctx.author.add_roles(rank_role)
    else:
      rank = ranked["tier"]
      rank_role = discord.utils.get(guild.roles,name=f"{rank}")
      for Tier in ranks:
        if Tier in ctx.author.roles:
          ctx.author.remove_roles(guild.roles, name=f'{Tier}')
            
      await ctx.author.add_roles(rank_role)
      rank_role = discord.utils.get(guild.roles, name="EUNE")
      await ctx.author.add_roles(rank_role)
      
    if username == "198103940481417216" and rank == "SILVER":
      embed = discord.Embed(
        title='Rank Update Complete!',
        description='EPITELOUS RE MLK PIGES SILVER',
        colour=discord.Colour.green())
      await ctx.send(embed=embed)
    embed = discord.Embed(
      title='Rank Update Complete!',
      description=f'Your discord role has been updated!',
      colour=discord.Colour.green())
    await ctx.send(embed=embed)


### Error Handling Area ###

  @register.error
  async def reg_error(self, ctx, error):
      if isinstance(error, commands.MissingRequiredArgument):
          if error.param.name == 'username':
              embed = discord.Embed(
                  title="Error",
                  description=
                  f"A name must be given. the command is {prefix}register <Summoner Name> ",
                  colour=discord.Colour.red())
              await ctx.send(embed=embed)
      elif isinstance(error, commands.CommandInvokeError):
          embed = discord.Embed(
              title='Missing Permissions',
              description=
              'You shuld place the bot on top of the ranks to be working',
              colour=discord.Colour.red())
          await ctx.send(embed=embed)
      else:
          raise error

  @force_register.error
  async def force_reg_error(self, ctx, error):
      if isinstance(error, commands.MissingRequiredArgument):
          if error.param.name == 'username' or error.param.name == 'member' or error.param.name == 'id':
              embed = discord.Embed(
                  title="Error",
                  description=
                  f"A name must be given. the command is {prefix}freg **ID** **SummonerName** **DiscordName**",
                  colour=discord.Colour.red())
              await ctx.send(embed=embed)
      elif isinstance(error, commands.CommandInvokeError):
          embed = discord.Embed(
              title='Error',
              description=
              f'Some arguments are missing try {prefix}freg **ID** **SummonerName** **DiscordName**',
              colour=discord.Colour.red())
          await ctx.send(embed=embed)
      else:
          raise error

  @update.error
  async def update_error(self, ctx, error):
    if KeyError(error, commands.CommandInvokeError):
      embed = discord.Embed(
          title="Account not registered",
          description=f"You don't have an account linked to your discord account type **{prefix}register** and Bind your league account to discord",
          colour=discord.Colour.red())
    else:
      raise error
      await ctx.send(embed=embed)


  @profile.error
  async def prof_error(self, ctx, error):
      if isinstance(error, commands.MissingRequiredArgument):
          if error.param.name == 'username':
              embed = discord.Embed(
                  title="Error",
                  description=
                  "You have to give me your Summoner name from league to be able to show your stats.",
                  colour=discord.Colour.red())
              await ctx.send(embed=embed)
      elif isinstance(error, commands.CommandInvokeError):
          embed = discord.Embed(
              title="Error",
              description=
              "Summoner name Doesn't Exist Check if you typed it right or it has a weird symbol",
              colour=discord.Colour.red())
          await ctx.send(embed=embed)
      else:
          raise error
        
  @me.error
  async def me_error(self, ctx, error):
      if KeyError(error, commands.CommandInvokeError):
          embed = discord.Embed(
              title="Account not registered",
              description=
              f"You don't have an account linked to your discord account type **{prefix}register** and Bind your league account to discord",
              colour=discord.Colour.red())
          await ctx.send(embed=embed)
      elif isinstance(error, commands.CommandInvokeError):
          embed = discord.Embed(
              title="Error",
              description=
              "Summoner name Doesn't Exist Check if you typed it right or it has a weird symbol or [**For the owner, The API has Expiered cause riot is gay**]",
              colour=discord.Colour.red())
          await ctx.send(embed=embed)
      else:
          raise error


def setup(client):
  client.add_cog(league(client))