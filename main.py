import asyncio
from datetime import datetime
from log import Log
import discord
from discord.ext import commands

# 공부하자 서버 id는 1217667923720667209
# todo채널 id는 1217692949970812979

# 로그 설정
log = Log()
log.log_info('Information message')
log.log_error('Error message')

# 토큰 가져오기
try:
    with open("config/token.txt", 'r') as f:
        token = f.readline().strip()
except FileNotFoundError:
    log.log_error("Token file not found.")
    exit()


async def send_message_at_time(message, channel_id, send_time):
    await client.wait_until_ready()
    channel = client.get_channel(channel_id)

    while not client.is_closed():
        current_time = datetime.now().strftime("%H:%M")
        print("현재 시간:", current_time)
        if current_time == send_time:
            await channel.send(message)

        await asyncio.sleep(60)  # 60초(1분)마다 현재 시간을 확인하여 특정 시간에 도달했는지 확인합니다.


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'{self.user}가 준비 완료!')
        await self.change_presence(status=discord.Status.online, activity=discord.Game("대기중"))
        await send_message_at_time("얘들아 TODO했니?", 1217692949970812979, "21:00")

    async def on_message(self, message):
        if message.author == self.user:  # 봇 메시지 무시
            return
        print(f"message.author:{message.author}\n"
              f"message.guild:{message.guild}\n"
              f"message.guild.id:{message.guild.id}\n"
              f"message.channel:{message.channel}\n"
              f"message.channel.id:{message.channel.id}\n"
              f"message.content:{message.content}\n"
              f"-------------------------------"
              f"\n")


# Intents 설정
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
description = '구냥'
activity = discord.Game("초기 개발")

client = MyClient(intents=intents)
client.run(token)
