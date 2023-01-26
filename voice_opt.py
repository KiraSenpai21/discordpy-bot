async def create_channel(guild, channel_name, category_name="VOICE CHANNELS", user_limit=None):
  category = get_category_by_name(guild, category_name)
  await guild.create_voice_channel(channel_name, category=category, user_limit=user_limit)
  channel = get_channel_by_name(guild, channel_name)
  return channel

def get_channel_by_name(guild, channel_name):
  channel = None
  for c in guild.channels:
    if c.name == channel_name:
      channel = c
      break
  return channel
  
def get_category_by_name(guild, category_name):
  category=None
  for c in guild.categories:
    if c.name == category_name:
      category = c
      break
  return category