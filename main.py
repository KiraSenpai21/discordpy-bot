import discord
from discord import app_commands
from riotwatcher import LolWatcher, ApiError
from getChampionNameByID import get_champions_name
from threading import Thread
import requests
import datetime
import random
import json
import time
import os

# VERSION: 1.2.20

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
    try:
        live_game = lol_watcher.spectator.by_summoner(region=region, encrypted_summoner_id=id)
        participants = live_game['participants']
        
        # Separate participants into blue team and red team
        blue_team = [p for p in participants if p['teamId'] == 100]
        red_team = [p for p in participants if p['teamId'] == 200]
        
        # Get summoner names, ranks, and champion names for each team
        blue_summoners = []
        red_summoners = []
        for participant in participants:
            summoner_name = participant['summonerName']
            summoner_id = participant['summonerId']
            rank = 'Unranked'
            try:
                league_entries = lol_watcher.league.by_summoner(region=region, encrypted_summoner_id=summoner_id)
                for entry in league_entries:
                    if entry['queueType'] == 'RANKED_SOLO_5x5':
                        rank = f'{entry["tier"]} {entry["rank"]} - {entry["leaguePoints"]} LP'
                        break
            except ApiError as err:
                if err.response.status_code == 404:
                    rank = 'Unranked'
                else:
                    raise
            champion_id = participant['championId']
            champion_name = get_champions_name(champion_id)
            summoner_info = {'name': summoner_name ,'rank': rank, 'champion_name': champion_name}
            if participant['teamId'] == 100:
                blue_summoners.append(summoner_info)
            else:
                red_summoners.append(summoner_info)
        
        # Combine summoner info into two strings, one for each team
        blue_list = '\n'.join([f'**{s["name"]}** ({s["rank"]}) \n {s["champion_name"]}' for s in blue_summoners])
        red_list = '\n'.join([f'**{s["name"]}** ({s["rank"]}) \n {s["champion_name"]}' for s in red_summoners])
        
        # Create the embed with two columns
        embed = discord.Embed(title=f'{username} is live playing right now', description='', color=discord.Colour.purple())
        embed.add_field(name='Blue Team', value=blue_list, inline=True)
        embed.add_field(name='Red Team', value=red_list, inline=True)
        
        await ctx.followup.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(title=f'{username} is not in a game', description='this summoner is not currently in a game.', color=discord.Colour.purple())
        await ctx.followup.send(embed=embed)
        raise(e)
    
@tree.command(name='getrole',description='gives the rank you got as a role',guild=discord.Object(id=821479008574242918))
async def profile(ctx: discord.Interaction, username: str):
    region = 'eun1'
    # API = os.environ['LApi']
    API = 'RGAPI-c4b15a16-a68a-4520-9892-3affeb489db3'
    lol_watcher = LolWatcher(API)
    me = lol_watcher.summoner.by_name(region, username)
    ranked_stats = lol_watcher.league.by_summoner(region, me['id'])
    code = me['profileIconId']
    ranked_solo = None
    ranked_flex = None
    unranked = False
    both = False

    # VERIFICATION CODE
    ver_pic = random.randint(0, 10)
    if ver_pic == code:
        ver_pic = random.randint(0, 10)

    embed = discord.Embed(
        title='Need further Verification',
        description='You need to verify it\'s your account first by changing the profile picture to the one shown below. Please note that you have only 60 seconds.',
        color=discord.Colour.purple()
    )
    embed.set_thumbnail(
        url=f"https://raw.communitydragon.org/latest/game/assets/ux/summonericons/profileicon{ver_pic}.png"
    )
    await ctx.response.send_message(embed=embed)

    endTime = datetime.datetime.now() + datetime.timedelta(seconds=60)
    while ver_pic != code:
        time.sleep(2)
        me = lol_watcher.summoner.by_name(region, username)
        code = me['profileIconId']
        if code == ver_pic or datetime.datetime.now() >= endTime:
            break

    if datetime.datetime.now() >= endTime:
        embed = discord.Embed(
            title='Timed out!',
            description="Your time is over, you haven't changed your profile picture in League. You can try again though.",
            color=discord.Colour.red()
        )
        await ctx.followup.send(embed=embed)

    # UNRANKED ROLES GIVEN AUTOMATICALLY
    if not ranked_stats:
        unranked = True

    # CHECKING WITH IFS IF THE USER HAS ANY RANK
    else:
        for rank in ranked_stats:
            if rank['queueType'] == 'RANKED_SOLO_5x5':
                ranked_solo = rank
            if rank['queueType'] == 'RANKED_FLEX_SR':
                ranked_flex = rank

        if ranked_solo and ranked_flex:
            both = True

    member = ctx.user
    guild = ctx.guild

    if unranked:
        role = discord.utils.get(guild.roles, name='UNRANKED')
        await member.add_roles(role)
        await ctx.followup.send('Role added: UNRANKED')

    elif both:
        solo_role = discord.utils.get(guild.roles, name=ranked_solo['tier'])
        flex_role = discord.utils.get(guild.roles, name=ranked_flex['tier'])
        await member.add_roles(solo_role, flex_role)
        if code == ver_pic:
            embed = discord.Embed(
                title='Successfully Verified!',
                description=f"You have successfully verified your account. you received role's {ranked_solo['tier']} {ranked_flex['tier']}.",
                color=discord.Colour.green()
            )
            await ctx.followup.send(embed=embed)

    elif ranked_solo:
        solo_role = discord.utils.get(guild.roles, name=ranked_solo['tier'])
        await member.add_roles(solo_role)
        if code == ver_pic:
            embed = discord.Embed(
                title='Successfully Verified!',
                description=f"You have successfully verified your account. you received role {ranked_solo['tier']}",
                color=discord.Colour.green()
            )
            await ctx.followup.send(embed=embed)

    elif ranked_flex:
        flex_role = discord.utils.get(guild.roles, name=ranked_flex['tier'])
        await member.add_roles(flex_role)
        if code == ver_pic:
            embed = discord.Embed(
                title='Successfully Verified!',
                description=f"You have successfully verified your account. you received role {ranked_flex['tier']}.",
                color=discord.Colour.green()
            )
            await ctx.followup.send(embed=embed)


@tree.command(name='updaterank', description='Updates the ranked roles for the user',guild=discord.Object(id=821479008574242918))
async def updaterank(ctx: discord.Interaction):
    member = ctx.user
    guild = ctx.guild
    region = 'eun1'
    API = os.environ['LApi']
    lol_watcher = LolWatcher(API)
    username = "username"  # Replace with the actual username or a way to retrieve it
    try:
        me = lol_watcher.summoner.by_name(region, username)
        ranked_stats = lol_watcher.league.by_summoner(region, me['id'])
    except ApiError as e:
        await ctx.response.send_message(f"An error occurred: {e}")
        return

    unranked = not ranked_stats
    ranked_solo = None
    ranked_flex = None
    both = False

    if not unranked:
        for rank in ranked_stats:
            if rank['queueType'] == 'RANKED_SOLO_5x5':
                ranked_solo = rank
            if rank['queueType'] == 'RANKED_FLEX_SR':
                ranked_flex = rank

        if ranked_solo and ranked_flex:
            both = True

    if unranked:
        role = discord.utils.get(guild.roles, name='UNRANKED')
        await member.remove_roles(role)
        await ctx.response.send_message('Role removed: UNRANKED')

    elif both:
        solo_role = discord.utils.get(guild.roles, name=ranked_solo['tier'])
        flex_role = discord.utils.get(guild.roles, name=ranked_flex['tier'])

        roles_to_remove = []
        roles_to_add = []

        for role in member.roles:
            if role.name in ['IRON', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'DIAMOND']:
                roles_to_remove.append(role)

        roles_to_add.extend([solo_role, flex_role])

        await member.remove_roles(*roles_to_remove)
        await member.add_roles(*roles_to_add)

        await ctx.response.send_message(f'Roles updated: {ranked_solo["tier"]}, {ranked_flex["tier"]}')

    elif ranked_solo:
        solo_role = discord.utils.get(guild.roles, name=ranked_solo['tier'])

        roles_to_remove = []
        roles_to_add = []

        for role in member.roles:
            if role.name in ['IRON', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'DIAMOND']:
                roles_to_remove.append(role)

        roles_to_add.append(solo_role)

        await member.remove_roles(*roles_to_remove)
        await member.add_roles(*roles_to_add)

        await ctx.response.send_message(f'Role updated: {ranked_solo["tier"]}')

    elif ranked_flex:
        flex_role = discord.utils.get(guild.roles, name=ranked_flex['tier'])

        roles_to_remove = []
        roles_to_add = []

        for role in member.roles:
            if role.name in ['IRON', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'DIAMOND']:
                roles_to_remove.append(role)

        roles_to_add.append(flex_role)

        await member.remove_roles(*roles_to_remove)
        await member.add_roles(*roles_to_add)

        await ctx.response.send_message(f'Role updated: {ranked_flex["tier"]}')

client.run(os.environ["DISCORD_TOKEN"])
