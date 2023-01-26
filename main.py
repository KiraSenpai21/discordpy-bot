import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='$', intents=intents)
client.remove_command('help')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title="Error",
                              description="Command not found",
                              colour=discord.Colour.red())
        await ctx.send(embed=embed)
      
@client.event
async def on_ready():
    print('Bot is now initialized... and online', f"latency: {round(client.latency * 1000)}ms")
    try:
        for filename in os.listdir("./cogs"):
          if filename.endswith(".py") and filename != "__init__.py":
             await client.load_extension(f'cogs.{filename[:-3]}')
    except Exception as e:
        print(e)

@client.event
async def on_member_join(member, reason=None):
    embed = discord.Embed(
      title = "Welcome To Unbroken!",
      colour = discord.Colour.red()
    )
    embed.set_author(name=f"{member.name}")
    embed.set_thumbnail(url=member.avatar_url)
    await member.send(embed=embed)
    role = 833336572749414420
    eune = 828880287705595954
    await member.add_roles((member.guild.get_role(role)), reason=reason)
    await member.add_roles((member.guild.get_role(eune)), reason=reason)
  
# Bot Commands #

# @client.command()
# @commands.has_permissions(manage_messages=True)
# async def clear(ctx, amount=5):
#     """clears the chat """
#     try:
#         await ctx.channel.purge(limit=amount + 1)
#         embed = discord.Embed(title=f"Cleared {amount} messages!",
#                               colour=discord.Colour.green())
#         await ctx.send(embed=embed)
#     except None:
#         pass


@client.command()
async def help(ctx):
    embed = discord.Embed(
        title="Bot Commands",
        description="This are the Commands for the Unbroken Bot Prefix ( $ )",
        colour=discord.Colour.green())
    embed.set_footer(text="UnBroken Bot 2021")
    embed.set_author(
        name="UnBroken",
        icon_url=
        "https://lolstatic-a.akamaihd.net/frontpage/apps/prod/mid-season-magic/en_GB/4e9063b04dcba600ab1718f8af28dba18e380220/assets/img/elemental-dragon-fire-thumb.png"
    )
    embed.add_field(
        name="League Of Legends Comamnds:",
        value=
        "$profile {summoner name} \n $register {summoner name} \n $me \n $delete_acc {summoner name}"
    )
    embed.add_field(
        name="Admin Commands:",
        value=
        "$kick {user} \n $ban {user} \n $ping \n $load {extension} \n $reload {extension} \n $unload {extesion}"
    )
    embed.add_field(name="Music Commands:",
                    value="$play {song name} \n $pause \n $skip \n $next ")
    await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(manage_messages=True)
async def ping(ctx):
    """Shows the Latency between the server and the bot"""
    embed = discord.Embed(title=f"latency: {round(client.latency * 1000)}ms",
                          colour=discord.Colour.green())
    await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(administrator=True)
async def load(ctx, extension):
    """Loads Extensions"""
    client.load_extension(f"cogs.{extension}")
    embed = discord.Embed(title=f"( {extension} ) Loaded.",
                          colour=discord.Colour.green())
    await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(administrator=True)
async def unload(ctx, extension):
    """Unloads extensions"""
    client.unload_extension(f"cogs.{extension}")
    embed = discord.Embed(title=f"( {extension} ) unloaded Successfully.",
                          colour=discord.Colour.green())
    await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(administrator=True)
async def reload(ctx, extension):
    """Reloads existing Extensions"""
    client.reload_extension(f"cogs.{extension}")
    embed = discord.Embed(title=f"( {extension} ) Reloaded Successfully.",
                          colour=discord.Colour.green())
    await ctx.send(embed=embed)


@reload.error
async def handler_reload(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        if error.param.name == 'extension':
            embed = discord.Embed(
                title="Error",
                description="You forgot to give the name of the extesion",
                colour=discord.Colour.red())
            await ctx.send(embed=embed)
    raise error


@client.command()
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.remove_roles(mutedRole)
    embed = discord.Embed(title="Unmuted",
                          description=f" unmuted-{member.mention}",
                          color=discord.Colour.green())
    await ctx.send(embed=embed)


@client.command()
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")
    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")
        for channel in guild.channels:
            await channel.set_permissions(mutedRole,
                                          speak=False,
                                          send_messages=False,
                                          read_message_history=True,
                                          read_messages=False)
    embed = discord.Embed(title="Muted",
                          description=f"{member} was muted ",
                          color=discord.Colour.green())
    embed.add_field(name="reason:", value=reason, inline=False)
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)
client.run(os.environ["DISCORD_TOKEN"])
