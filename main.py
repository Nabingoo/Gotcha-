
import os
import discord
from discord.ext import commands


bot = commands.Bot(command_prefix = "-")


bot.sniped_messages = {}

@bot.event
async def on_ready():
    print(len(bot.guilds))
    await bot.change_presence(activity=discord.Game(name="Guess who's back, back again."))

@bot.event
async def on_message_delete(message: discord.Message):
    image = None
    #If there's any attachments, Grab the last one.
    if message.attachments:
        image = await message.attachments[-1].to_file(use_cached=True)
    #Add to sniped messages dictionary.
    bot.sniped_messages[message.channel.id] = (message.content, message.author, message.channel.name, message.created_at, image)


@bot.command()
async def s(ctx):
    try:
        contents, author, channel_name, time, image = bot.sniped_messages[ctx.channel.id]
    except:
        await ctx.channel.send("I don't see anything.")
        return

    embed = discord.Embed(description=contents, color=discord.Color.orange(), timestamp=time)
    #If fetched message had an image
    if image:
        #Set it as the embed image via attachment
        embed.set_image(url=f"attachment://{image.filename}")
    embed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url)
    embed.set_footer(text=f"Deleted in : #{channel_name}")

    await ctx.channel.send(embed=embed, file=image)
bot.run(os.getenv('TOKEN'))
