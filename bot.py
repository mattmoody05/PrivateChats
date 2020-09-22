# imports
import discord
from discord.ext import commands
import os

# functions
def FileLength(fname):
        with open(fname) as f:
                for i, l in enumerate(f):
                        pass
        return i + 1

def IDFromArg(arg):
    UserID = arg
    UserID = UserID.replace("<","")
    UserID = UserID.replace(">","")
    UserID = UserID.replace("@","")
    UserID = UserID.replace("!","")
    UserID = int(UserID)
    return UserID

# constants
BOTPREFIX = "."
BOTTOKEN = ""
ICONURL = "https://img.icons8.com/dusk/64/000000/private2.png"
Role1 = 757982334120099851
Role2 = 757982382912569344
Role3 = 757982420065714206
TChannel1 = 757982721120403496
TChannel2 = 757983326824038461
TChannel3 = 757983383841275934

# declaring the client object
client = commands.Bot(command_prefix = BOTPREFIX)

# removing the default help command so that a better one can be made using embeds
client.remove_command("help")

# changing the bot's status to "Listening to $help" and printing that the bot has logged in without any issues
@client.event
async def on_ready():
    ListeningTo = discord.Activity(type=discord.ActivityType.listening, name=".help")
    await client.change_presence(status=discord.Status.online, activity=ListeningTo)
    print('We have logged in as {0.user}'.format(client))


# testing command
@client.command()
async def ping(ctx):
    await ctx.send("pong")


# creating, closing or clearing(mod) a private room
@client.command()
async def private(ctx, arg):
    # ======= creating a new room =======
    if arg == "new":
        ChatFree = 0
        AlreadyOwner = False
        for i in range(3):
            OwnerText = open("./rooms/{0}/owner.txt".format(i + 1), "r")
            Owner = OwnerText.readline()
            OwnerText.close()
            if Owner == str(ctx.author.id):
                AlreadyOwner = True
            elif Owner == "open":
                ChatFree = i + 1

        if AlreadyOwner == False:   
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
            WelcomeEmbed.add_field(name = "Inviting people", value = "Type '.invite @user' to invite someone to your room")
            WelcomeEmbed.add_field(name = "Closing room", value = "Type '.private close' to close the room")
            WelcomeEmbed.add_field(name = "Privacy info", value = "Only the people you invite can access the voice channel and text channel that you are currently in. When you close the room, or when the room automatically closes, all of your conversation will be deleted and there will be no way to recover it. Please save any information you wish to keep.", inline = False)
            WelcomeEmbed.add_field(name = "Message Deletion", value="When you run '.private close', all messages in the channel that you have been using will be deleted. This action is not visible on the screen because the role to access the private channel will have been removed. The source code is availiable on github if you would like to inspect this.", inline=False)
            WelcomeEmbed.add_field(name = "Failsafes", value = "If for any reasons the messages do not clear properly, read message history has been turned off, this means that no-one is able to read any past messages from the channel.", inline=False)
            
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
        else:
            AlreadyOwnerEmbed = discord.Embed(
                colour = discord.Colour.light_gray()
            )
            AlreadyOwnerEmbed.set_author(name = "You already own a room, please do not open another one", icon_url=ICONURL)
            await ctx.send(embed = AlreadyOwnerEmbed)
            
           
    # ======= closing the room =======
    elif arg == "close":
        ChatOwned = 0
        for i in range (3):
            OwnerText = open("./rooms/{0}/owner.txt".format(i + 1), "r")
            temp = OwnerText.readline()
            if temp != "open":
                Owner = int(temp)
                OwnerText.close()
                OwnerUser = client.get_user(Owner)
                if OwnerUser == ctx.author:
                    ChatOwned = i + 1
        
        ClosingEmbed = discord.Embed(
            colour = discord.Colour.light_gray()
        )
        ClosingEmbed.set_author(name = "Your private room was successfully closed", icon_url=ICONURL)

        if ChatOwned == 1:
            Channel = client.get_channel(TChannel1)
            await ctx.send(embed = ClosingEmbed)
            MemberFileLen = FileLength("./rooms/1/members.txt")
            MemberFile = open("./rooms/1/members.txt", "r")
            role = ctx.guild.get_role(Role1)
            for i in range(MemberFileLen):
                CurrentMember = ctx.guild.get_member(int(MemberFile.readline()))
                await CurrentMember.remove_roles(role)
            MemberFile.close()
            OwnerText = open("./rooms/1/owner.txt", "w")
            OwnerText.writelines("open")
            OwnerText.close()
            os.remove("./rooms/1/members.txt")
            await Channel.purge()
        elif ChatOwned == 2:
            Channel = client.get_channel(TChannel2)
            await ctx.send(embed = ClosingEmbed)
            MemberFileLen = FileLength("./rooms/2/members.txt")
            MemberFile = open("./rooms/2/members.txt", "r")
            role = ctx.guild.get_role(Role2)
            for i in range(MemberFileLen):
                CurrentMember = ctx.guild.get_member(int(MemberFile.readline()))
                await CurrentMember.remove_roles(role)
            MemberFile.close()
            OwnerText = open("./rooms/2/owner.txt", "w")
            OwnerText.writelines("open")
            OwnerText.close()
            os.remove("./rooms/2/members.txt")
            await Channel.purge()
        elif ChatOwned == 3:
            Channel = client.get_channel(TChannel3)
            await ctx.send(embed = ClosingEmbed)
            MemberFileLen = FileLength("./rooms/3/members.txt")
            MemberFile = open("./rooms/3/members.txt", "r")
            role = ctx.guild.get_role(Role3)
            for i in range(MemberFileLen):
                CurrentMember = ctx.guild.get_member(int(MemberFile.readline()))
                await CurrentMember.remove_roles(role)
            MemberFile.close()
            OwnerText = open("./rooms/3/owner.txt", "w")
            OwnerText.writelines("open")
            OwnerText.close()
            os.remove("./rooms/3/members.txt")
            await Channel.purge()
        else:
            ErrorEmbed = discord.Embed(
                colour = discord.Colour.light_gray()
            )
            ErrorEmbed.set_author(name = "You do not own a room", icon_url = ICONURL)
            await ctx.send(embed = ErrorEmbed)

    
    # ======= mod only: reseting all the rooms to the open state
    elif arg == "clear":
        for i in range(3):
            user = client.get_user(486508895368511490)
            if user == ctx.author:
                OwnerText = open("./rooms/{0}/owner.txt".format(i + 1), "w")
                Owner = OwnerText.writelines("open")
                OwnerText.close()
                # ========== Need to clear member files too here ==============
            else:
                ErrorEmbed = discord.Embed(
                    colour = discord.Colour.light_gray()
                )
                ErrorEmbed.set_author(name = "You do not have permission to use this command", icon_url = ICONURL)
                await ctx.send(embed = ErrorEmbed)

    else:
        ErrorEmbed = discord.Embed(
            colour = discord.Colour.light_gray()
        )
        ErrorEmbed.set_author(name = "Please input a valid command", icon_url = ICONURL)
        await ctx.send(embed = ErrorEmbed)


# command to invite someone to the room
@client.command()
async def invite(ctx, arg):
    ChatOwned = 0
    for i in range (3):
        OwnerText = open("./rooms/{0}/owner.txt".format(i + 1), "r")
        temp = OwnerText.readline()
        if temp != "open":
            Owner = int(temp)
            OwnerText.close()
            OwnerUser = client.get_user(Owner)
            if OwnerUser == ctx.author:
                ChatOwned = i + 1
    
    if ChatOwned == 1:
        MemberText = open("./rooms/1/members.txt", "a")
        MemberText.writelines("\n" + str(IDFromArg(arg)))
        MemberText.close()
        user = ctx.guild.get_member(IDFromArg(arg))
        role = ctx.guild.get_role(Role1)
        await user.add_roles(role)
        UserAddEmbed = discord.Embed(
            colour = discord.Colour.light_gray()
        )
        UserAddEmbed.set_author(name = "{0} has been added to the room".format(user.name), icon_url = ICONURL)
        Channel = ctx.guild.get_channel(TChannel1)
        await Channel.send(embed = UserAddEmbed)
        DMEmbed = discord.Embed(
            colour = discord.Colour.light_gray()
        )
        DMEmbed.set_author(name = "You have been added to a private room", icon_url=ICONURL)
        DMEmbed.add_field(name = "Server", value = "limeSMP")
        DMEmbed.add_field(name = "Added by", value = ctx.author.name)
        DMEmbed.add_field(name = "Room number", value="1")
        await user.send(embed = DMEmbed)
    elif ChatOwned == 2:
        MemberText = open("./rooms/2/members.txt", "a")
        MemberText.writelines("\n" + str(IDFromArg(arg)))
        MemberText.close()
        user = ctx.guild.get_member(IDFromArg(arg))
        role = ctx.guild.get_role(Role2)
        await user.add_roles(role)
        UserAddEmbed = discord.Embed(
            colour = discord.Colour.light_gray()
        )
        UserAddEmbed.set_author(name = "{0} has been added to the room".format(user.name), icon_url = ICONURL)
        Channel = ctx.guild.get_channel(TChannel2)
        await Channel.send(embed = UserAddEmbed)
        DMEmbed = discord.Embed(
            colour = discord.Colour.light_gray()
        )
        DMEmbed.set_author(name = "You have been added to a private room", icon_url=ICONURL)
        DMEmbed.add_field(name = "Server", value = "limeSMP")
        DMEmbed.add_field(name = "Added by", value = ctx.author.name)
        DMEmbed.add_field(name = "Room number", value="2")
        await user.send(embed = DMEmbed)
    elif ChatOwned == 3:
        MemberText = open("./rooms/3/members.txt", "a")
        MemberText.writelines("\n" + str(IDFromArg(arg)))
        MemberText.close()
        user = ctx.guild.get_member(IDFromArg(arg))
        role = ctx.guild.get_role(Role3)
        await user.add_roles(role)
        UserAddEmbed = discord.Embed(
            colour = discord.Colour.light_gray()
        )
        UserAddEmbed.set_author(name = "{0} has been added to the room".format(user.name), icon_url = ICONURL)
        Channel = ctx.guild.get_channel(TChannel3)
        await Channel.send(embed = UserAddEmbed)
        DMEmbed = discord.Embed(
            colour = discord.Colour.light_gray()
        )
        DMEmbed.set_author(name = "You have been added to a private room", icon_url=ICONURL)
        DMEmbed.add_field(name = "Server", value = "limeSMP")
        DMEmbed.add_field(name = "Added by", value = ctx.author.name)
        DMEmbed.add_field(name = "Room number", value="3")
        await user.send(embed = DMEmbed)
    else:
        ErrorEmbed = discord.Embed(
            colour = discord.Colour.light_gray()
        )
        ErrorEmbed.set_author(name = "You do not own a room", icon_url = ICONURL)
        await ctx.send(embed = ErrorEmbed)


@client.command()
async def help(ctx):
    HelpEmbed = discord.Embed(
        colour = discord.Colour.light_gray()
    )
    HelpEmbed.set_author(name = "PrivateBot help", icon_url = ICONURL)
    HelpEmbed.add_field(name = "Getting room", value = "Type '.private new' to get a room")
    HelpEmbed.add_field(name = "Inviting people", value = "Type '.invite @user' to invite someone to your room")
    HelpEmbed.add_field(name = "Closing room", value = "Type '.private close' to close the room that you are in")
    HelpEmbed.add_field(name = "Privacy info", value = "Only the people you invite can access the voice channel and text channel that you are currently in. When you close the room, or when the room automatically closes, all of your conversation will be deleted and there will be no way to recover it. Please save any information you wish to keep.", inline = False)
    HelpEmbed.add_field(name = "Message Deletion", value="When you run '.private close', all messages in the channel that you have been using will be deleted. This action is not visible on the screen because the role to access the private channel will have been removed. The source code is availiable on Github if you would like to inspect this.", inline=False)
    HelpEmbed.add_field(name = "Failsafes", value = "If for any reasons the messages do not clear properly, read message history has been turned off, this means that no-one is able to read any past messages from the channel.", inline=False)
    await ctx.send(embed = HelpEmbed)



client.run(BOTTOKEN)