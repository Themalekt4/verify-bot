import discord
from discord.ext import commands
from discord.ext.commands import *
import os

bot = discord.Bot()
client = commands.Bot(command_prefix="-")
client.remove_command("help")

theServerId = [931985720858542080]

@client.event
async def on_ready():
 await client.change_presence(status=discord.Status.dnd, activity=discord.Game(name='Welcome to the server!'))


@client.event
async def on_member_join(member):
    Unverified = discord.utils.get(member.guild.roles, id = 959133886095433788)
    await member.add_roles(Unverified)
    verificationChannel = discord.utils.get(member.guild.channels, id = 950080290250956860)
    await verificationChannel.send(f"Hello {member.mention}! Welcome to **{member.guild.name}**! God Bless You! \n\n Please answer the questions provided, and a staff member will be right with you! please mention the verification team role when you are done. \n\n 1. Are you Christian? \n 2. Who is Jesus to you? \n If you answered yes to the first question, what is your denomination? If you answered no, do you have any religious beliefs, and what are they? \n 4. Have you read and agreed to the rules? \n 5. Will you respect the staff members and their decisions? \n 6. Where did you get the invite to this server from? (please be specific) \n 7. What do rules #1 and #6 say in your own words? \n 8. What reason do you have to join this server?")
    await member.send(f"Hello {member.mention} and welcome to {member.guild.name}! Be sure to answer the verification questions in <#950080290250956860> in order to get access to the rest of the server.")


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
      await ctx.send(":x: **I couldn't find that command!**")
    if isinstance(error, MissingPermissions):
      await ctx.send(":x: **You don't have permission to use this command!**")
    if isinstance(error, MissingRequiredArgument):
      await ctx.send("**You forgot to specify your command!**")



@client.command(aliases=['av'])
async def avatar(ctx, *,  avamember : discord.Member):
    userAvatarUrl = avamember.display_avatar
    embedav = discord.Embed(title="Here is their avatar:", Description="lol", color=0xffffff)
    embedav.set_image(url=f'{userAvatarUrl}')
    await ctx.send(embed=embedav)


@avatar.error
async def avatar_error(ctx, error):
  if isinstance(error, Exception):
    await ctx.send(f"{Exception}")

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member, *, reason=None):
  await user.kick(reason=reason)
  await ctx.send(f"**{user} has been kicked successfully!**", delete_after=5)

@client.command(aliases=['h'])
async def help(ctx):
  embed2 = discord.Embed(Title="helpmenu", color=0xac3d5f)
  embed2.add_field(name="Bot in developement!", value="Hello! I'm the official bot for this server, and I will have more commands soon! I currently only have certain moderation commands set up.", inline=False)
  embed2.set_thumbnail(text="Thanks for being patient!")
  await ctx.send(embed=embed2)

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, user: discord.Member, *, reason=None):
  await user.ban(reason=reason)
  await ctx.send(f"**{user.mention} has been bannned successfully!**", delete_after=5)
  await ctx.message.delete()


@client.command(aliases=['dl'])
@commands.has_permissions(manage_roles = True)
@commands.guild_only()
async def delrole(ctx, role: discord.Role):
    await client.delete.role(role.server, role)
    await ctx.send(f"The role {role.name} has been deleted!")

@client.command(aliases=['make_role', 'ar', 'addrole'])
@commands.has_permissions(manage_roles=True)
@commands.guild_only()
async def create_role(ctx, *, name):
	guild = ctx.guild.roles()
	await guild.create.role(name=name)
	await ctx.send(f'Role `{name}` has been created')


@client.command()
async def userinfo(ctx, user = discord.User):
  acctdate = user.created_at
  mention = user.mention
  banner = user.banner
  accolor = user.accent_color
  id = user.id
  userinfoembed = discord.Embed(title=f"About {user}:", description=f"\n **Mention:** {mention} \n **Account Age:** {acctdate} \n **ID:** {id}", color=accolor)
  userinfoembed.set_thumbnail(url=f"{user.display_avatar}")
  await ctx.send(embed=userinfoembed)


@client.command(aliases=['wipeclean', 'purge', 'clean'])
@commands.has_permissions(manage_messages = True)
@commands.guild_only()
async def clear(ctx, amount=5):
   await ctx.channel.purge(limit=amount)
   await ctx.message.delete()
   await ctx.send("**Messages Purged!**", delete_after=5)

@client.command()
async def ping(ctx):
    embedVar = discord.Embed(title="Pong", color=0x00ff00)
    embedVar.add_field(name="Latency",
                       value=str(round(client.latency * 1000 ) + "ms"),
                       inline=False)
    await ctx.send(embed=embedVar)


@client.slash_command()
@commands.has_permissions(kick_members=True)
async def arrest(ctx, member : discord.Member):
  arrested_role = ctx.guild.get_role(941893822957375489)
  verified_role = ctx.guild.get_role(944060470350999612)
  await member.add_roles(arrested_role)
  await member.remove_roles(verified_role)
  await ctx.respond(member.mention + " **Arrested!** :rage: :police_officer:")

@client.slash_command()
@commands.has_permissions(kick_members=True)
async def setfree(ctx, member : discord.Member):
  arrested_role = ctx.guild.get_role(941893822957375489)
  verified_role = ctx.guild.get_role(944060470350999612)
  await member.add_roles(verified_role)
  await member.remove_roles(arrested_role)
  await ctx.respond(member.mention + " **has been let go. Warning all sane people.**")


@client.slash_command()
@commands.has_permissions(manage_roles = True)
async def verify(ctx, member: discord.Member):
    unverified_role = ctx.guild.get_role(959133886095433788)
    verified_role = ctx.guild.get_role(944060470350999612)
    generalChannel = discord.utils.get(member.guild.channels, id =931985720858542083)
    await member.add_roles(verified_role)
    await member.remove_roles(unverified_role)
    await generalChannel.send(f"Hello {member.mention}, may the grace of our Lord and Saviour Jesus Christ be with you. God bless you. Please pick your <#946907048677879848> and enjoy your time here! :grin:")
    await ctx.respond(f"**{member.mention} has been verified by {ctx.author.mention}!**")

@client.command(aliases=['v', 'ver'])
@commands.has_permissions(manage_roles = True)
async def verifying(ctx, member: discord.Member):
    unverified_role = ctx.guild.get_role(959133886095433788)
    verified_role = ctx.guild.get_role(944060470350999612)
    generalChannel = discord.utils.get(member.guild.channels, id =931985720858542083)
    await member.add_roles(verified_role)
    await member.remove_roles(unverified_role)
    await generalChannel.send(f"Hello {member.mention}, may the grace of our Lord and Saviour Jesus Christ be with you. God bless you. Please pick your <#946907048677879848> and enjoy your time here! :grin:")
    await ctx.send(f"**{member.mention} has been verified by {ctx.author.mention}!**")

@client.command()
@commands.guild_only()
async def sus(ctx):
  await ctx.send("**AMONGUS!**", delete_after=0.3)
  await ctx.message.delete()


token = os.environ.get('TOKEN')
client.run(token)