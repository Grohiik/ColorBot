import discord
from discord.ext import commands
from secrets import Token as Token

bot = commands.Bot(command_prefix="!")
role_add_channel_id = 750036407757832242


@bot.event
async def on_message(message):
    if bot.user == message.author:
        return
    if message.channel.id == role_add_channel_id:
        await bot.process_commands(message)
        await message.delete(delay=10)


@bot.command(name="färg", help="lägg till en färg")
async def color(payload):
    if payload.channel.id == role_add_channel_id:
        member = payload.author
        guild = member.guild
        check = True
        color = discord.Colour(int(payload.message.content[6:12], base=16))
        for role in member.roles:
            if str(member.id) == role.name:
                await role.edit(colour=(color))
                await payload.channel.send(
                    content=f"Ändrade {member.display_name} färg till {color.value}",
                    delete_after=10,
                )
                check = False
                break
        if check:
            await guild.create_role(
                name=str(member.id), color=color, reason="färg roll"
            )
            for role in guild.roles:
                if str(member.id) == role.name:
                    await member.add_roles(role)
                    await payload.channel.send(
                        content=f"Ändrade {member.display_name} färg till {color.value}",
                        delete_after=10,
                    )
                    break


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send("detta kommandet finns inte", delete_after=15)
        await ctx.delete(delay=10)


@bot.event
async def on_command_error2(ctx, error):
    await ctx.send("kommand error", delete_after=15)
    await ctx.delete(delay=10)


# command to test if the bot is running
@bot.command(name="test", help="test")
async def test(ctx):
    response = "Jag är online!"
    await ctx.send(response)


# command to test if the bot is running
@bot.command(name="ping", help="test")
async def test2(ctx):
    response = "pong 🏓"
    await ctx.send(response)


# print a message if the bot is online
@bot.event
async def on_ready():
    print("bot connected")
    # change status to online
    await bot.change_presence(activity=discord.Game("FÄRG"))


bot.run(Token)
