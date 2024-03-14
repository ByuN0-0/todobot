import asyncio
from datetime import datetime
import logging
import discord
from discord.ext import commands

# 로그 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# 토큰 가져오기
try:
    with open("config/token.txt", 'r') as f:
        token = f.readline().strip()
except FileNotFoundError:
    logger.error("Token file not found.")
    exit()

# Intents 설정
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
description = '구냥'

bot = commands.Bot(command_prefix='?', description=description, intents=intents)


# 공부하자서버 id는 1217667923720667209
# todo채널 id는 1217692949970812979
@bot.event
async def on_ready():
    print(f'{bot.user}가 준비 완료!')
    await send_message_at_time("얘들아 TODO했니?", 1217692949970812979, "21:00")


async def send_message_at_time(message, channel_id, send_time):
    await bot.wait_until_ready()
    channel = bot.get_channel(channel_id)
    print("1분지남")

    while not bot.is_closed():
        current_time = datetime.now().strftime("%H:%M")
        print("현재 시간:", current_time)
        if current_time == send_time:
            await channel.send(message)

        await asyncio.sleep(60)  # 60초(1분)마다 현재 시간을 확인하여 특정 시간에 도달했는지 확인합니다.


@bot.event
async def on_message(message):
    if message.author == bot.user:  # 봇 자신이 보낸 메시지는 무시합니다.
        return
    print(f"message.author:{message.author}\n"
          f"message.guild:{message.guild}\n"
          f"message.guild.id:{message.guild.id}\n"
          f"message.channel:{message.channel}\n"
          f"message.channel.id:{message.channel.id}\n"
          f"message.content:{message.content}\n"
          f"-------------------------------"
          f"\n")

    await bot.process_commands(message)


bot.run(token)
