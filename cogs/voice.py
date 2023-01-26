from discord.ext import commands
from voice_opt import create_channel, get_category_by_name


class voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.bot:
            return

        if after.channel is not None:
            if after.channel.name == "Join to interview":
                channel = await create_channel(after.channel.guild,
                                               f"{member.name}'s - Interview",
                                               category_name="Interviews")
                if channel is not None:
                    await member.move_to(channel)

        if before.channel is not None:
            if before.channel.category.id == get_category_by_name(
                    before.channel.guild, "Interviews").id:
                pass
                if len(before.channel.members) == 0:
                    await before.channel.delete()


async def setup(client):
    await client.add_cog(voice(client))
