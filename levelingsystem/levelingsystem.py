import discord
from discord import ui
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Bot
from discord import Permissions, channel, guild, utils
from discord import Embed
from discord.utils import get
from discord import Interaction

bot = commands.Bot(command_prefix=">", intents=discord.Intents.all())
intents = discord.Intents.default() 
intents.message_content = True
intents.guilds = True
intents.members = True
client = discord.Client(intents = intents)

TOKEN = "your_token_here"


@bot.event 
async def on_ready():
    print("Bot is up and ready!")
    try:
        synced = await bot.tree.sync() 
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


@bot.event
async def on_message(message):
    
    try:
        if message.author == bot.user:
            return
        if message.channel.name == "spam":
            return
        if message.channel.name == "random-stuff":
            return
        # Get the author ID of the message
        author_id = message.author.id
        server_id = message.guild.id
        with open("message_count.txt", "r") as f:
            lines = f.readlines()
            if lines != []:
                lines = lines[0].split("*")
        with open("message_count.txt", "r") as f:
            content = f.read()
        with open("message_count.txt", "a") as f:

            
                
            listeee = []
            for i in lines:
                if str(author_id) in i and str(server_id) in i:
                    listeee.append(i)
                    break
            goomba = False
            if listeee != []:
                goomba = True
                key, value = listeee[0].split(": ") 
                goomba_id = {key: int(value)+1}
                
            else:
                
                f.write(f"{str(author_id)}_{str(server_id)}: 1*")
                goomba_id = f"{str(author_id)}_{str(server_id)}: 1"
                
                key, value = goomba_id.split(": ")
                goomba_id = {key: value}
                
        if goomba == True:
            with open("message_count.txt", "w") as f:
                content = content.replace(f"{str(author_id)}_{str(server_id)}: {value}", f"{key}: {int(value)+1}")
                
                f.write(content)
                
        with open("levels.txt", "r") as f:
            lines = f.readlines()
            if lines != []:
                lines = lines[0].split("*")
        with open("levels.txt", "r") as f:
            contents = f.read()
        with open("levels.txt", "a") as f:
            if int(goomba_id[f"{str(author_id)}_{str(server_id)}"])%50 == 0:
                found = False
                for i in lines:
                    if ":" in i:
                        ia = i.split(":")
                    else:
                        continue
                    
                    if ia[0] in str(goomba_id):
                        found = True
                        key, value = i.split(": ")
                        curent = {key: value}
                        current = value
                        size_messages = len(str(goomba_id[f"{str(author_id)}_{str(server_id)}"]))   
                        counter = 0   
                        for i in range(0, size_messages-1):
                            if counter != 0:
                                level = level + str(str(goomba_id[f"{str(author_id)}_{str(server_id)}"]))[counter]
                            else:
                                level = str(str(goomba_id[f"{str(author_id)}_{str(server_id)}"]))[counter]
                            counter += 1
                        break
                if found == False:
                    f.write(f"{str(author_id)}_{str(server_id)}: 1*")
                    return
            else: 
                return
        
        with open("levels.txt", "w") as f:
                contents = contents.replace(f"{str(author_id)}_{str(server_id)}: {current}", f"{str(author_id)}_{str(server_id)}: {int(level)//5}")
                f.write(contents)
                
    except Exception as e:
        print(e)



@bot.tree.command(name="level", description="Checks your current level in this server")
@app_commands.checks.has_permissions(manage_channels=True)
@app_commands.describe(user="What user to see the level of?")
async def current_level(interaction: Interaction, user: discord.Member=None):
    if user == None:
        user_id = interaction.user.id
    else:
        user_id = user.id
    server_id = interaction.guild_id
    found = False
    try:
        with open("levels.txt", "r") as f:
            lines = f.readlines()
            lines = lines[0].split("*")
            for i in lines:
                if f"{user_id}_{server_id}" in i:
                    found = True
                    key, value = i.split(": ")
                    i = {key: value}
                    level = i[f"{user_id}_{server_id}"]
                    break
        if found == True:
            if user == None or user == interaction.user:
                await interaction.response.send_message(f"Your current level is: {level}", ephemeral=True)
            else:
                await interaction.response.send_message(f"{user.mention}'s current level is: {level}", ephemeral=True)
        else:
            if user == None or user == interaction.user:
                await interaction.response.send_message(f"Your current level is: 0", ephemeral=True)
            else:
                await interaction.response.send_message(f"{user.mention}'s current level is: 0", ephemeral=True)   
    except:
        if user == None or user == interaction.user:
            await interaction.response.send_message(f"Your current level is: 0", ephemeral=True)
        else:
            await interaction.response.send_message(f"{user.mention}'s current level is: 0", ephemeral=True)   

bot.run(TOKEN)
