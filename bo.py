import discord
import requests
from datetime import datetime
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
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('새벽 감성 타기'))

@bot.event
async def on_message(message):     #안녕으로 시작하는 문장에 반응
    if message.author == bot.user:
        return
    
    if message.content.startswith('안녕'):
        await message.channel.send('안녕하세요!')
        await message.author.send("{} | {} 유저님, 환영합니다.".format(message.author, message.author.mention))
    
    await bot.process_commands(message)

@bot.command(name="고양이")   #랜덤 고양이 사진 보내기
async def 고양이(ctx):
    response = requests.get("https://api.thecatapi.com/v1/images/search")
    data = response.json()
    image_url = data[0]['url']
    await ctx.send(image_url)

@bot.command(name="강아지")    #랜덤 강아지 사진 보내기
async def 강아지(ctx):
    response = requests.get("https://api.thedogapi.com/v1/images/search")
    data = response.json()
    image_url = data[0]['url']
    await ctx.send(image_url)

@bot.command(name="청소")    #청소 개수를 입력하여 개수만큼 메세지 삭제
async def 청소(ctx, amount: int):
    if amount <= 99:
        await ctx.channel.purge(limit=amount+1)
        await ctx.send(f"{amount}개의 메시지가 삭제되었습니다.", delete_after=5)
    else:
        await ctx.send("한 번에 최대 99개의 메세지를 삭제할 수 있어요!")

@bot.command(name="시간")   #현재시간 띄우기
async def 시간(ctx):
    now = datetime.now()
    current_time = now.strftime("%Y년 %m월 %d일 %H시 %M분 %S초")
    await ctx.send(f"현재 시간은 {current_time}입니다.")

@bot.command(name="날씨")  #날씨... 이거 어렵더라구요
async def 날씨(ctx):
    locdata = requests.get("https://ipinfo.io/")
    location = locdata.json()
    loc = location["city"]
    api_key = "25fd02ed63bdc22ad6f08381eeda43fd"  # OpenWeatherMap API 키를 입력하세요.
    url = f"http://api.openweathermap.org/data/2.5/weather?q={loc}&appid={api_key}&units=metric"
    responce = requests.get(url)
    data = responce.json()
    temperature = data["main"]["temp"]
    temp_feel = data["main"]["feels_like"]
    weather = data["weather"]
    print(weather)
    
    await ctx.send(f"```\n\n현재 지역 : {loc}\n\n현재 온도 : {temperature} °C\n\n체감 온도 : {temp_feel} °C\n\n현재 날씨 : {weather} \n\n```")

bot.run(Token)