import os 
import discord
import requests
from discord.ext import commands
from webserver import keep_alive

intents = discord.Intents().all()
client = commands.Bot(command_prefix="$", help_command=None, intents=intents)

@client.event
async def on_ready():
    print("Bot ready")


@client.command()
async def proxy(ctx, prxy=None, limit=None):
    if prxy is None:
        em = discord.Embed(title="Usage", description="$proxy [socks4 / socks5 / http] [limit]")
        await ctx.send(embed=em)
        return
    
    if limit is None:
        limit = 10
    else:
        limit = int(limit)

    scraped = 0
    f = open("proxies.txt", "a+")
    f.truncate(0)
    r = requests.get(f'https://api.proxyscrape.com/?request=displayproxies&proxytype={prxy}')
    proxies = []
    for proxy in r.text.split('\n'):
        proxy = proxy.strip()
        if proxy:
            proxies.append(proxy)
    for p in proxies[:limit]:
        scraped = scraped + 1 
        f.write((p)+"\n")
    f.close()
    
    em = discord.Embed(title=f"Scraped Proxies", description=f"Scraped {scraped} {prxy} proxies.")
    await ctx.send(file=discord.File('./proxies.txt'), embed=em)
    
token = input('Enter your Discord Bot token: ')
keep_alive()    
client.run(token)