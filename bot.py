# imports
import discord
from discord.ext import commands
import os

# constants
BOTPREFIX = "/"
BOTTOKEN = ""
ICONURL = "https://i.ibb.co/6WvNLY4/lime2-Copy-Copy-Copy.png"
Role1 = 756231144525004921
Role2 = 756231219946979408
Role3 = 756231231141576816
TChannel1 = 756230599307689984
TChannel2 = 756232007327154337
TChannel3 = 756232034195603476

# declaring the client object
client = commands.Bot(command_prefix = BOTPREFIX)

# removing the default help command so that a better one can be made using embeds
client.remove_command("help")

# changing the bot's status to "Listening to $help" and printing that the bot has logged in without any issues
@client.event
async def on_ready():
    ListeningTo = discord.Activity(type=discord.ActivityType.listening, name="/help")
    await client.change_presence(status=discord.Status.online, activity=ListeningTo)
    print('We have logged in as {0.user}'.format(client))



@client.command()
async def private(ctx, arg):
    # ======= creating a new room =======
    if arg == "new":
        ChatFree = 0
        for i in range(3):
            OwnerText = open("./rooms/{0}/owner.txt".format(i + 1), "r")
            Owner = OwnerText.readline()
            OwnerText.close()
            if Owner == "open":
                ChatFree = i + 1
            
        if ChatFree == 0:
            ErrorEmbed = discord.Embed(
                colour = discord.Colour.light_gray()
            )
            ErrorEmbed.set_author(name = "PrivateBot Error", icon_url = ICONURL)
            ErrorEmbed.add_field(name = "Error Message", value = "All rooms are occupied, or there has been an error. If you are not able to see anyone currently in a room, please send a dm to Modmail")
            await ctx.send(embed = ErrorEmbed)
        else:
            OwnerText = open("./rooms/{0}/owner.txt".format(ChatFree), "w")
            OwnerText.writelines(str(ctx.message.author.id))
            OwnerText.close()
            OwnerText = open("./rooms/{0}/members.txt".format(ChatFree), "w")
            OwnerText.writelines(str(ctx.message.author.id))
            OwnerText.close()

        WelcomeEmbed = discord.Embed(
            colour = discord.Color.light_gray()
        )
        WelcomeEmbed.set_author(name = "Welcome to your PrivateBot room", icon_url = ICONURL)
        WelcomeEmbed.add_field(name = "Inviting people", value = "Type '/private @user' to invite someone to your room")
        WelcomeEmbed.add_field(name = "Closing room", value = "Tyoe '/private close' to close the room")
        WelcomeEmbed.add_field(name = "Privacy info", value = "Only the people you invite can access the voice channel and text channel that you are currently in. When you close the room, or when the room automatically closes, all of your conversation will be deleted and there will be no way to recover it. Please save any information you wish to keep.", inline = False)
        
        if ChatFree == 1:
            role = ctx.guild.get_role(Role1)
            user = ctx.author
            await user.add_roles(role)
            Channel = client.get_channel(TChannel1)
            # new code
            await Channel.send(ctx.message.author.mention + " welcome to your private room!")
            await Channel.send(embed = WelcomeEmbed)
        elif ChatFree == 2:
            role = ctx.guild.get_role(Role2)
            user = ctx.author
            await user.add_roles(role)
            Channel = client.get_channel(TChannel2)
            # new code
            await Channel.send(ctx.message.author.mention + " welcome to your private room!")
            await Channel.send(embed = WelcomeEmbed)
        elif ChatFree == 3: 
            role = ctx.guild.get_role(Role3)
            user = ctx.author
            await user.add_roles(role)
            Channel = client.get_channel(TChannel3)
            # new code
            await Channel.send(ctx.message.author.mention + " welcome to your private room!")
            await Channel.send(embed = WelcomeEmbed)
        
            

    # ======= closing the room =======
    elif arg == "close":
        print("close")
    # ======= mod only: reseting all the rooms to the open state
    elif arg == "clear":
        for i in range(3):
            OwnerText = open("./rooms/{0}/owner.txt".format(i + 1), "w")
            Owner = OwnerText.writelines("open")
            OwnerText.close()

        
    # ======= inviting someone to the room =======
    else:
        print("user")


@client.command()
async def help(ctx):
    HelpEmbed = discord.Embed(
        colour = discord.Colour.light_gray()
    )
    HelpEmbed.set_author(name = "PrivateBot help", icon_url = ICONURL)
    HelpEmbed.add_field(name = "Getting room", value = "Type '/private new' to get a room")
    HelpEmbed.add_field(name = "Inviting people", value = "Type '/private @user' to invite someone to your room")
    HelpEmbed.add_field(name = "Closing room", value = "Tyoe '/private close' to close the room that you are in")
    await ctx.send(embed = HelpEmbed)

@client.command()
async def hello(ctx):
    await ctx.send("hello " + ctx.message.author.mention)

client.run(BOTTOKEN)