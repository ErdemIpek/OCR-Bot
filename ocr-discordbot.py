import discord
from discord.ext import commands
import datetime
import requests
import json
import os
from boto.s3.connection import S3Connection
s3 = S3Connection(os.environ['DISCORD_TOKEN'], os.environ['API_KEY'])

#https://ocr.space/OCRAPI used api for ocr.
def ocr_space_url(url, overlay=False, api_key='helloworld', language='eng'):
    payload = {'url': url,
               'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }
    r = requests.post('https://api.ocr.space/parse/image',
                      data=payload,
                      )
    return r.content.decode()

bot = commands.Bot(command_prefix='$')
#Commands
@bot.command()
async def ocr(ctx,url="default",lang="ENG"):
    try:
        api_call = ocr_space_url(url=url,api_key=os.environ['API_KEY'],language=lang)
        results_object = json.loads(api_call)#the ocr result as python object.
        text = results_object["ParsedResults"][0]["ParsedText"]
        await ctx.send('Result:\n\n {0}'.format(text))
    except:
         await ctx.send("Please check the command and try again.\nIf you are having any trouble please write '$commands'")
         

@bot.command()
async def commands(ctx):
    embed=discord.Embed(title="OCR-Bot", description="Available commands", color=0x00ccff)
    embed.add_field(name="$ocr 'url' 'language'", value="Convert image to text", inline=False)
    embed.add_field(name="$lang", value="Shows available languages for ocr", inline=False)
    embed.add_field(name="$commands", value="See available commands", inline=True)
    embed.set_footer(text="https://github.com/ErdemIpek/OCR-DiscordBot")
    await ctx.send(embed=embed)
@bot.command()
async def lang(ctx):
    await ctx.send("\nArabic=ara\nBulgarian=bul\nChinese(Simplified)=chs\nChinese(Traditional)=cht\nCroatian = hrv\nCzech = cze\nDanish = dan\nDutch = dut\nEnglish = eng\nFinnish = fin\nFrench = fre\nGerman = ger\nGreek = gre\nHungarian = hun\nKorean = kor\nItalian = ita\nJapanese = jpn\nPolish = pol\nPortuguese = por\nRussian = rus\nSlovenian = slv\nSpanish = spa\nSwedish = swe\nTurkish = tur")

#Events
@bot.event
async def on_ready():
    print('Logged on as {0}!'.format(bot.user))
@bot.event 
async def on_command_error(ctx,error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send("That command wasn't found! Sorry :(")

bot.run(os.environ['DISCORD_TOKEN'])#bot token
