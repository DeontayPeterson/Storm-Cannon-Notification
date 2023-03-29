from party_key import key
from searcher import make_call
import discord
import asyncio
import cv2 as cv
from PIL import ImageGrab

#sftp://

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"{client.user} Logged in now!")

@client.event
async def on_message(message):
    condition = True
    if message.author == client.user:
        return
    
    if message.content.startswith('sc'):
        while condition:
            output = make_call()
            result = output[0]
            loc = output[1]
            if not result:
                await asyncio.sleep(5)
            else:
                for index,item in enumerate(result):
                    region_name = loc[index]
                    if item['iconType'] == 59:
                        await message.channel.send(("@everyone" , item))
                        await message.channel.send("@everyone" + f"STORM CANNON in {region_name}")
                            
                    elif item['iconType'] == 60:
                        await message.channel.send(("@everyone" , item))
                        await message.channel.send("@everyone" + f"intel center in {region_name}")
                    else:
                        await message.channel.send((item , f"{region_name}"))
                        
                await asyncio.sleep(5)
                 
                

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('p'):
        ss = ImageGrab.grab()
        await message.channel.send(ss)


bot_token = key
client.run(bot_token)



    
