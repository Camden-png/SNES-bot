logo = """
 ____ ____ ____ ____ _________ ____ ____ ____
||S |||N |||E |||S |||       |||b |||o |||t ||
||__|||__|||__|||__|||_______|||__|||__|||__||
|/__\|/__\|/__\|/__\|/_______\|/__\|/__\|/__\|"""

import os
import sys
import time
import socket
import asyncio
import platform

try: import discord
except ImportError:
    print("Error: no Discord library found!")
    sys.exit(1)

try: import aioconsole
except:
    print("Error: no Aioconsole library found!")
    sys.exit(1)

channel = None
message = None

address = ("127.0.0.1", 51914)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

wait = 0.05
vertical = [0, 0]
horizontal = [0, 0]

b = [0x83, 0x85, 0x86, 0x84, 0x88, 0x89, 0x87, 0x8a, 0x80, 0x81]
c = ["u", "d", "l", "r", "a", "b", "x", "y", "select", "start"]
r = ["\u2b06", "\u2b07", "\u2b05", "\u27a1", "\U0001f534", "\U0001f7e1", "\U0001f535", "\U0001f7e2", "\u25b6", "\u23f8"]


bot = discord.Client()

def clear():
    if platform.system() == "Windows": os.system("cls")
    else: os.system("clear")

async def start(token): global bot; await asnycio.gather(*[query(), bot.start(token)])

def printer(string): print(f"Error: no {string} found!"); return 1

def main():
    global bot, logo
    clear()
    name = "Token.txt"
    try: file = open(name, "r")
    except: return printer(name)
    token = file.read()
    if not token: return printer("token")
    file.close()
    print(f"{logo[1:]}\n")
    loop = asyncio.get_event_loop()
    try: loop.run_until_complete(start(token))
    except: clear()
    loop.run_until_complete(on_end())
    loop.run_until_complete(bot.logout())

async def query():
    global wait
    while True:
        try:
            value = await aioconsole.ainput("Enter button press duration: ")
            try:
                value = float(value)
                if value >= 0:
                    temp = value = abs(value)
                    if temp == int(temp): temp = int(temp)
                    print(f"New duration: {temp}")
                    wait = value
                    if wait == 0: wait = 0.05
                else: raise
            except: pass
        except: break

@bot.event
async def on_ready():
    global r, bot, channel, message
    guild = bot.guilds[0]
    for text_channel in guild.text_channels:
        if text_channel.name == "snes-commands":
            channel = text_channel
            break
    if not channel: channel = await guild.create_text_channel("snes-commands")
    await channel.purge()
    string = "Use the emoticons or type U, D, L, R, A, B, X, Y, SELECT, START!\nBy Camden!"
    embed = discord.Embed(title = "SNES-controller", description = string, color = 0x4f43ae)
    embed.set_thumbnail(url = "https://i.imgur.com/ZV8cLxa.png")
    message = await channel.send(embed = embed)
    for reaction in r: await message.add_reaction(reaction)

async def on_end():
    global b, sock, address, channel
    await channel.purge()
    await channel.send(embed = discord.Embed(description = "Offline  :octagonal_sign:", color = 0x4f43ae))
    for button in b: sock.sendto(bytearray([0x01] * 2 + [button] + [0x00] * 4), address)

async def controller_input(button):
    global sock, address, vertical, horizontal
    packet = bytearray([0x01] * 2 + [button] + [0x00] * 3 + [0xff])
    if button not in [0x88, 0x89, 0x87, 0x8a]:
        if vertical != [0, 0] and packet != vertical[1]:
            vertical[1][-1] = 0x00
            sock.sendto(vertical[1], address)
        elif horizontal != [0, 0] and packet != horizontal[1]:
            horizontal[1][-1] = 0x00
            sock.sendto(horizontal[1], address)
        temporary = [-1, -1]
        if button in [0x83, 0x85]:
            vertical[0] += 1
            vertical[1] = packet
            temporary[0] = vertical[0]
        else:
            horizontal[0] += 1
            horizontal[1] = packet
            temporary[1] = horizontal[0]
        sock.sendto(packet, address)
        await asyncio.sleep(wait)
        if temporary[0] == vertical[0] or temporary[1] == horizontal[0]:
            packet[-1] = 0x00
            sock.sendto(packet, address)
    else:
        sock.sendto(packet, address)
        await asyncio.sleep(0.05)
        packet[-1] = 0x00
        sock.sendto(packet, address)

@bot.event
async def on_reaction_add(reaction, user):
    global b, r, bot, message
    if message == reaction.message and user != bot.user:
        await reaction.remove(user)
        if reaction in r: await controller_input(b[r.index(reaction)])

@bot.event
async def on_message(message):
    global b, c, bot, channel
    if message.channel == channel and message.author != bot.user:
        lower = message.content.lower()
        if lower in c:
            await message.add_reaction(":white_check_mark:")
            await controller_input(b[c.index(lower)])
        else: await message.add_reaction(":octagonal_sign:")

sys.exit(main())
