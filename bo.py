import discord
import requests
from discord.ext import commands
from disco_token import Token

intents = discord.Intents.default()
intents.typing = True
intents.presences = True
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix='!')

@bot.event
async def on_ready():
    print(f"봇이 성공적으로 로그인 되었습니다. 봇 이름 : {bot.user.name}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content.startswith('안녕'):
        await message.channel.send('안녕하세요!')
    
    await bot.process_commands(message)

@bot.command()
async def 핑(ctx):
    await ctx.send('pong')

@bot.command(name="고양이")
async def 고양이(ctx):
    response = requests.get("https://api.thecatapi.com/v1/images/search")
    data = response.json()
    image_url = data[0]['url']
    await ctx.send(image_url)

@bot.command(name="강아지")
async def 강아지(ctx):
    response = requests.get("https://api.thedogapi.com/v1/images/search")
    data = response.json()
    image_url = data[0]['url']
    await ctx.send(image_url)

@bot.command(name="청소")
async def 청소(ctx, amount: int):
    if amount <= 99:
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(f"{amount}개의 메시지가 삭제되었습니다.", delete_after=5)
    else:
        await ctx.send("한 번에 최대 99개의 메세지를 삭제할 수 있어요!")

bot.run(Token)