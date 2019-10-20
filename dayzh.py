import discord
import asyncio
import random
import json
import requests
import xmltodict
from time import time
import datetime
from mcstatus import MinecraftServer

client = discord.Client()
token = "token"
mcserver = MinecraftServer.lookup("mcpepsi.online")

staff = [000000000000000000]

afklist = []

usercmd = ["/서버상태","/잠수","/제안","/신고","/디데이","/단어검색","/도움말","/핑"]
mancmd = ["/투표","/패치","/공지","/처벌"]

red = discord.Color.from_rgb(255, 0, 0)
green = discord.Color.from_rgb(0, 255, 0)
blue = discord.Color.from_rgb(0, 0, 255)

@client.event
async def on_ready():
    print("Online")
    while not client.is_closed():
        await client.change_presence(status=discord.Status.online, activity=discord.Game(name="상태 확인 중 | DayZH"))
        try:
            mcserver.ping()
        except:
            await client.change_presence(status=discord.Status.online, activity=discord.Game(name="서버 오프라인 | DayZH"))
        else:
            await client.change_presence(status=discord.Status.online, activity=discord.Game(name=f"서버 온라인 | {str(mcserver.status().players.online)}명 접속 중"))
        await asyncio.sleep(60)
    
@client.event
async def on_message(message):
    random_color = discord.Color.from_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    if not message.author.bot:
        if message.channel.id == 620131472786980894 and not message.author.id == 625205925724028928:
            if message.content.startswith("```") and message.content[len(message.content) - 3:] == "```":
                await message.delete()
                naeyong = message.content.replace("`", "").replace("@everyone","").replace("@here","")
                embed = discord.Embed(title=f":tools: **패치 내용**", description=f"{naeyong}", color=random_color, timestamp=datetime.datetime.utcnow())
                if len(message.attachments) >= 1:
                    embed.add_field(name="**사진 또는 동영상**", value="아래 첨부.", inline=True)
                    embed.set_image(url=message.attachments[0].url)
                embed.set_footer(text="for everyone", icon_url=client.user.avatar_url)
                await message.channel.send(embed=embed)
                return
        if message.author.id in afklist:
            embed = discord.Embed(title=":flushed: **움찔!**", description="아... 뭐야... 잘 잤는데... 아...", color=random_color, timestamp=datetime.datetime.utcnow())
            embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
            await message.channel.send(embed=embed)
            afklist.remove(message.author.id)
            if ''.join(message.content[1:].split()[0]) == "잠수":
                return
        if not message.content.startswith("/"):
            return
        command = ''.join(message.content[1:].split()[0])
        commandline = ' '.join(message.content.split()[1:])
        if command == "서버상태":
            async with message.channel.typing():
                try:
                    ping = mcserver.ping()
                except:
                    online = False
                else:
                    online = True
                embed = discord.Embed(title=":thumbsup: **서버 상태 확인 완료!**", description=f"{message.author.name}님을 위해 제가 특별히 서버 상태를 가져왔습니다.\n아래에서 확인하세요!", color=random_color, timestamp=datetime.datetime.utcnow())
                if online == False:
                    embed.add_field(name=":cry: **안타깝게도 서버 상태는**", value="__오프라인__", inline=True)
                else:
                    motd = mcserver.status().description["text"]
                    embed.add_field(name=":laughing: **멋진 하루! 서버 상태는**", value="**__온라인__**", inline=True)
                    embed.add_field(name="**핑**", value=f"{str(ping)}ms", inline=True)
                    embed.add_field(name="**플레이어 수**", value=f"{str(mcserver.status().players.online)}/{str(mcserver.status().players.max)}", inline=True)
                    embed.add_field(name="**버전**", value=f"{str(mcserver.status().version.name)}", inline=True)
                    embed.add_field(name="**포트**", value=f"{str(mcserver.port)}", inline=True)
                    embed.add_field(name="**MOTD**", value=f"{str(motd)}", inline=True)
                embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
            await message.channel.send(embed=embed)
        elif command == "잠수":
            if len(commandline.split()) >= 1:
                reason = ' '.join(commandline.split()[0:])
                embed = discord.Embed(title=":zzz: **잠수 중...**", description=f"{message.author.display_name}님이 피곤하시대요... zZＺ\n사유는...\n```{reason}```", color=random_color, timestamp=datetime.datetime.utcnow())
                embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
                await message.channel.send(embed=embed)
            else:
                embed = discord.Embed(title=":zzz: **잠수 중...**", description=f"{message.author.display_name}님이 피곤하시대요... zZＺ\n사유는... 피곤해서...", color=random_color, timestamp=datetime.datetime.utcnow())
                embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
                await message.channel.send(embed=embed)
            afklist.append(message.author.id)
        elif command == "제안" or command == "오류신고":
            if len(commandline.split()) >= 1:
                embed = discord.Embed(title=":heart: **감사합니다!**", description="저희에게 말씀해주신 의견은 매우 유용하게 쓰일 것입니다!", color=random_color, timestamp=datetime.datetime.utcnow())
                embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
                await message.channel.send(embed=embed)
                channel = client.get_channel(626692409794756619)
                embed = discord.Embed(title=":ear: **제안이 도착했습니다.**", description="제안이 도착했어요!", color=random_color, timestamp=datetime.datetime.utcnow())
                embed.add_field(name="**보낸 사람**", value=f"{message.author} | {str(message.author.id)}", inline=True)
                naeyong = commandline.replace("``", "").replace("```", "")
                embed.add_field(name="**내용**", value=f"```\n{naeyong}\n```", inline=True)
                embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
                await channel.send(embed=embed)
            else:
                embed = discord.Embed(title=":question: **명령어가 잘못되었습니다!**", description="제안 명령어는 ``/제안 (제안사항)``으로 사용합니다.", color=red, timestamp=datetime.datetime.utcnow())
                embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
                await message.channel.send(embed=embed)
        elif command == "도움" or command == "도움말" or command == "헬프" or command == "헬프미":
            if message.author.id in staff:
                usercommands = ""
                for i in range(len(usercmd) - 1):
                    usercommands += f"{usercmd[i]}, "
                usercommands += usercmd[len(usercmd)-1]
                staffcommands = ""
                for i in range(len(mancmd) - 1):
                    staffcommands += f"{mancmd[i]}, "
                staffcommands += mancmd[len(mancmd) - 1]
                embed = discord.Embed(title=":sos: **Help me!**", description=f"현재 존재하는 유저 명령어:\n```\n{usercommands}\n```\n\n현재 존재하는 관리 명령어:\n```\n{staffcommands}\n```", color=random_color, timestamp=datetime.datetime.utcnow())
                embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
                await message.channel.send(embed=embed)
                return
            commands = ""
            for i in range(len(usercmd) - 1):
                commands += f"{usercmd[i]}, "
            commands += usercmd[len(usercmd) -1]
            embed = discord.Embed(title=":sos: **Help me!**", description=f"현재 존재하는 명령어:\n```\n{commands}\n```", color=random_color, timestamp=datetime.datetime.utcnow())
            embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
            await message.channel.send(embed=embed)
        elif command == "핑":
            channel = client.get_channel(635375607731060746)
            msg = await channel.send(content="핑 측정용")
            ping = (msg.created_at - message.created_at).total_seconds() * 1000
            embed = discord.Embed(title=":ping_pong: **퐁!**", description=f"저와 {message.author.display_name}님과의 시간차는 {str(ping)}ms입니다.", color=random_color, timestamp=datetime.datetime.utcnow())
            embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
            await message.channel.send(embed=embed)
        elif command == "신고" or command == "유저신고":
            if len(commandline.split()) >= 3:
                myname = commandline.split()[0].replace("``", "").replace("```", "")
                repname = commandline.split()[1].replace("``", "").replace("```", "")
                if myname == repname:
                    embed = discord.Embed(title=":question: **명령어가 잘못되었습니다!**", description="자신은 자신을 신고할 수 없습니다!", color=red, timestamp=datetime.datetime.utcnow())
                    embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
                    await message.channel.send(embed=embed)
                    return
                try:
                    response_my = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{myname}?at={str(int(time()))}").json()
                    myuuid = response_my["id"]
                    myname = response_my["name"]
                    response_rep = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{repname}?at={str(int(time()))}").json()
                    repuuid = response_rep["id"]
                    repname = response_rep["name"]
                except:
                    embed = discord.Embed(title=":exclamation: **오류가 발생하였습니다!**", description="UUID를 불러오는 데 오류가 발생하였습니다.\n또는, 입력한 닉네임이 잘못되었을 수도 있습니다.", color=red, timestamp=datetime.datetime.utcnow())
                    embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
                    await message.channel.send(embed=embed)
                    return
                if len(message.attachments) >= 1:
                    embed = discord.Embed(title=":heart: **감사합니다!**", description="저희에게 말씀해주신 신고는 관리자가 온라인이 되는 순간\n처리해 드리겠습니다. 신고 감사합니다.", color=random_color, timestamp=datetime.datetime.utcnow())
                    embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
                    await message.channel.send(embed=embed)
                    channel = client.get_channel(626692409794756619)
                    embed = discord.Embed(title=":mailbox_with_mail: **신고가 도착했습니다.**", description="신고가 도착했습니다.\n확인 바랍니다.", color=random_color, timestamp=datetime.datetime.utcnow())
                    embed.add_field(name="**보낸 사람**", value=f"{message.author} | {str(message.author.id)}", inline=True)
                    naeyong = ' '.join(commandline.split()[2:]).replace("``", "").replace("```", "")
                    embed.add_field(name="**신고하는 사람**", value=f"``{myname} | {myuuid}``", inline=True)
                    embed.add_field(name="**신고 대상**", value=f"``{repname} | {repuuid}``", inline=True)
                    embed.add_field(name="**내용**", value=f"```\n{naeyong}\n```", inline=True)
                    embed.add_field(name="**사진**", value="아래 첨부.", inline=True)
                    embed.set_image(url=message.attachments[0].url)
                    embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
                    await channel.send(embed=embed)
                else:
                    embed = discord.Embed(title=":question: **캡처본이 있으신가요?**", description="캡처된 증거가 있으시다면 __30초 내__로 올려주세요.\n30초가 지나면 증거 없이 신고됩니다.\n\n만약 캡처본이 없다면 ``아니오``라고 말해주세요.\n\n취소하려면 아무 말이나 입력해 주세요.", color=random_color, timestamp=datetime.datetime.utcnow())
                    embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
                    mm = await message.channel.send(embed=embed)
                    
                    def check(m):
                        return m.author == message.author and m.channel == message.channel

                    try:
                        msg = await client.wait_for('message', timeout=30.0, check=check)
                    except asyncio.TimeoutError:
                        embed = discord.Embed(title=":heart: **감사합니다!**", description="저희에게 말씀해주신 신고는 관리자가 온라인이 되는 순간\n처리해 드리겠습니다. 신고 감사합니다.", color=random_color, timestamp=datetime.datetime.utcnow())
                        embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
                        await mm.edit(embed=embed, content="캡처본 없이 신고됩니다.")
                        channel = client.get_channel(626692409794756619)
                        embed = discord.Embed(title=":mailbox_with_mail: **신고가 도착했습니다.**", description="신고가 도착했습니다.\n확인 바랍니다.", color=random_color, timestamp=datetime.datetime.utcnow())
                        embed.add_field(name="**보낸 사람**", value=f"{message.author} | {str(message.author.id)}", inline=True)
                        naeyong = ' '.join(commandline.split()[2:]).replace("``", "").replace("```", "")
                        embed.add_field(name="**신고하는 사람**", value=f"``{myname} | {myuuid}``", inline=True)
                        embed.add_field(name="**신고 대상**", value=f"``{repname} | {repuuid}``", inline=True)
                        embed.add_field(name="**내용**", value=f"```\n{naeyong}\n```", inline=True)
                        embed.add_field(name="**사진**", value="**없음**", inline=True)
                        embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
                        await channel.send(embed=embed)
                        await msg.delete()
                    else:
                        if msg.content == "아니오" or msg.content == "아니요":
                            embed = discord.Embed(title=":heart: **감사합니다!**", description="저희에게 말씀해주신 신고는 관리자가 온라인이 되는 순간\n처리해 드리겠습니다. 신고 감사합니다.", color=random_color, timestamp=datetime.datetime.utcnow())
                            embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
                            await mm.edit(embed=embed, content="캡처본 없이 신고됩니다.")
                            channel = client.get_channel(626692409794756619)
                            embed = discord.Embed(title=":mailbox_with_mail: **신고가 도착했습니다.**", description="신고가 도착했습니다.\n확인 바랍니다.", color=random_color, timestamp=datetime.datetime.utcnow())
                            embed.add_field(name="**보낸 사람**", value=f"{message.author} | {str(message.author.id)}", inline=True)
                            naeyong = ' '.join(commandline.split()[2:]).replace("``", "").replace("```", "")
                            embed.add_field(name="**신고하는 사람**", value=f"``{myname} | {myuuid}``", inline=True)
                            embed.add_field(name="**신고 대상**", value=f"``{repname} | {repuuid}``", inline=True)
                            embed.add_field(name="**내용**", value=f"```\n{naeyong}\n```", inline=True)
                            embed.add_field(name="**사진**", value="**없음**", inline=True)
                            embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
                            await channel.send(embed=embed)
                            await msg.delete()
                        elif len(msg.attachments) >= 1:
                            embed = discord.Embed(title=":heart: **감사합니다!**", description="저희에게 말씀해주신 신고는 관리자가 온라인이 되는 순간\n처리해 드리겠습니다. 신고 감사합니다.", color=random_color, timestamp=datetime.datetime.utcnow())
                            embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
                            await mm.edit(embed=embed)
                            channel = client.get_channel(626692409794756619)
                            embed = discord.Embed(title=":mailbox_with_mail: **신고가 도착했습니다.**", description="신고가 도착했습니다.\n확인 바랍니다.", color=random_color, timestamp=datetime.datetime.utcnow())
                            embed.add_field(name="**보낸 사람**", value=f"{message.author} | {str(message.author.id)}", inline=True)
                            naeyong = ' '.join(commandline.split()[2:]).replace("``", "").replace("```", "")
                            embed.add_field(name="**신고하는 사람**", value=f"``{myname} | {myuuid}``", inline=True)
                            embed.add_field(name="**신고 대상**", value=f"``{repname} | {repuuid}``", inline=True)
                            embed.add_field(name="**내용**", value=f"```\n{naeyong}\n```", inline=True)
                            embed.add_field(name="**사진**", value="아래 첨부.", inline=True)
                            embed.set_image(url=msg.attachments[0].url)
                            embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
                            await channel.send(embed=embed)
                            await msg.delete()
                        else:
                            embed = discord.Embed(title=":exclamation: **취소되었습니다.**", description="작업이 취소되었습니다.", color=red, timestamp=datetime.datetime.utcnow())
                            embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
                            await mm.edit(embed=embed)
            else:
                embed = discord.Embed(title=":question: **명령어가 잘못되었습니다!**", description="신고 명령어는 ``/신고 (자신의 닉네임) (신고하는 사람의 닉네임) (내용)``으로 사용합니다.\n\n*여기서의 '닉네임'은 인게임 닉네임을 뜻합니다.", color=red, timestamp=datetime.datetime.utcnow())
                embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
                await message.channel.send(embed=embed)
        elif command == "디데이":
            if len(commandline.split()) == 1:
                today = datetime.datetime.utcnow()
                if commandline == "오픈일":
                    day = "2019/10/13"
                elif commandline == "내년":
                    day = f"{str(today.year + 1)}/1/1"
                else:
                    if "/" in commandline:
                        day = commandline
                    else:
                        embed = discord.Embed(title=":question: **명령어가 잘못되었습니다!**", description="날짜는 ``(연도)/(달)/(일)`` 형식이어야 합니다.", color=red, timestamp=datetime.datetime.utcnow())
                        embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
                        await message.channel.send(embed=embed)
                        return
                if len(day.split("/")) > 3:
                    embed = discord.Embed(title=":question: **명령어가 잘못되었습니다!**", description="날짜는 ``(연도)/(달)/(일)`` 형식이어야 합니다.", color=red, timestamp=datetime.datetime.utcnow())
                    embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
                    await message.channel.send(embed=embed)
                    return
                try:
                    year = day.split("/")[0]
                    month = day.split("/")[1]
                    dayll = day.split("/")[2]
                    dayy = datetime.date(int(year), int(month), int(dayll))
                except KeyError:
                    embed = discord.Embed(title=":question: **명령어가 잘못되었습니다!**", description="날짜는 ``(연도)/(달)/(일)`` 형식이어야 합니다.", color=red, timestamp=datetime.datetime.utcnow())
                    embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
                    await message.channel.send(embed=embed)
                    return
                except ValueError:
                    embed = discord.Embed(title=":question: **명령어가 잘못되었습니다!**", description="날짜는 ``(연도)/(달)/(일)`` 형식이어야 합니다.", color=red, timestamp=datetime.datetime.utcnow())
                    embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
                    await message.channel.send(embed=embed)
                    return
                dday = today.toordinal() - dayy.toordinal()
                if str(dday).startswith("-"):
                    embed = discord.Embed(title=":calendar: **입력하신 날짜까지?**", description=f"오늘부터 {day}까지는 {str(dday)[1:]}일 남았습니다.", color=random_color, timestamp=datetime.datetime.utcnow())
                else:
                    embed = discord.Embed(title=":calendar: **입력하신 날짜까지?**", description=f"오늘부터 {day}까지는 {str(dday)}일 지났습니다.", color=random_color, timestamp=datetime.datetime.utcnow())
                embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
                await message.channel.send(embed=embed)
            else:
                embed = discord.Embed(title=":question: **명령어가 잘못되었습니다!**", description="디데이 계산 명령어는 ``/디데이 (연도/달/일)``으로 사용합니다.", color=red, timestamp=datetime.datetime.utcnow())
                embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
                await message.channel.send(embed=embed)
        elif command == "투표":
            if not message.author.id in staff:
                embed = discord.Embed(title=":exclamation: **권한이 부족합니다.**", description="이 명령어는 관리자만 사용할 수 있습니다.", color=red, timestamp=datetime.datetime.utcnow())
                embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
                await message.channel.send(embed=embed)
                return
            if len(commandline.split()) >= 4 and commandline.startswith("항목투표"):
                channel = client.get_channel(622386822571491360)
                title = commandline.split()[1].replace("`", "").replace("_", " ")
                votes = commandline.split()[2:]
                emote_str = {"1":":one:","2":":two:","3":":three:","4":":four:","5":":five:","6":":six:","7":":seven:","8":":eight:","9":":nine:"}
                emote = {"1":"1\N{COMBINING ENCLOSING KEYCAP}","2":"2\N{COMBINING ENCLOSING KEYCAP}","3":"3\N{COMBINING ENCLOSING KEYCAP}","4":"4\N{COMBINING ENCLOSING KEYCAP}","5":"5\N{COMBINING ENCLOSING KEYCAP}","6":"6\N{COMBINING ENCLOSING KEYCAP}","7":"7\N{COMBINING ENCLOSING KEYCAP}","8":"8\N{COMBINING ENCLOSING KEYCAP}","9":"9\N{COMBINING ENCLOSING KEYCAP}"}
                if len(votes) > 9:
                    embed = discord.Embed(title=":question: **명령어가 잘못되었습니다!**", description="투표 항목은 9개까지만 입력할 수 있습니다.", color=red, timestamp=datetime.datetime.utcnow())
                    embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
                    await message.channel.send(embed=embed)
                    return
                embed = discord.Embed(title=f":ballot_box_with_check: **{title}**", description="아래 항목들을 보고 투표해 주세요.", color=random_color, timestamp=datetime.datetime.utcnow())
                for i in range(len(votes)):
                    s = votes[i].replace("`", "").replace("_", " ")
                    emoji = emote_str[f"{str(i + 1)}"]
                    embed.add_field(name=f"{emoji}", value=f"{s}", inline=True)
                embed.set_footer(text="for everyone", icon_url=client.user.avatar_url)
                msg = await channel.send(embed=embed)
                for i in range(len(votes)):
                    emoji = emote[f"{str(i + 1)}"]
                    await msg.add_reaction(emoji)
            elif len(commandline.split()) >= 3 and commandline.startswith("찬반투표"):
                channel = client.get_channel(622386822571491360)
                title = commandline.split()[1].replace("`", "").replace("_", " ")
                naeyong = ' '.join(commandline.split()[2:])
                embed = discord.Embed(title=f":ballot_box_with_check: **{title}**", description=f"{naeyong}", color=random_color, timestamp=datetime.datetime.utcnow())
                msg = await channel.send(embed=embed)
                await msg.add_reaction("👍")
                await msg.add_reaction("👎")
            else:
                embed = discord.Embed(title=":question: **명령어가 잘못되었습니다!**", description="투표 명령어는 ``/투표 항목투표 (제목) (항목1) (항목2) ...`` 또는\n``/투표 찬반투표 (제목) (내용)``으로 사용합니다.\n\n*항목은 최대 9개까지 쓸 수 있습니다.\n*띄어쓰려면 언더바(_)를 사용하세요. *(예: DAY_ZH)*", color=red, timestamp=datetime.datetime.utcnow())
                embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
                await message.channel.send(embed=embed)
        elif command == "패치" or command == "패치노트":
            if not message.author.id in staff:
                embed = discord.Embed(title=":exclamation: **권한이 부족합니다.**", description="이 명령어는 관리자만 사용할 수 있습니다.", color=red, timestamp=datetime.datetime.utcnow())
                embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
                await message.channel.send(embed=embed)
                return
            if len(commandline.split()) >= 2:
                title = commandline.split()[0].replace("`", "").replace("*","").replace("_", " ")
                naeyong = ' '.join(commandline.split()[1:])
                if len(message.attachments) >= 1:
                    embed = discord.Embed(title=":white_check_mark: **패치노트 업로드 완료!**", description="올리신 패치노트는 <#620131472786980894>에 업로드되었습니다.", color=random_color, timestamp=datetime.datetime.utcnow())
                    embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
                    await message.channel.send(embed=embed)
                    channel = client.get_channel(620131472786980894)
                    embed = discord.Embed(title=f":tools: **{title}**", description=f"{naeyong}", color=random_color, timestamp=datetime.datetime.utcnow())
                    embed.add_field(name="**사진 또는 동영상**", value="아래 첨부.", inline=True)
                    embed.set_image(url=message.attachments[0].url)
                    embed.set_footer(text="for everyone", icon_url=client.user.avatar_url)
                    await channel.send(embed=embed)
                else:
                    embed = discord.Embed(title=":question: **사진 또는 동영상이 있으신가요?**", description="자료가 있으시다면 __30초 내__로 올려주세요.\n30초가 지나면 작업이 취소됩니다.\n\n만약 자료가 없다면 ``아니오``라고 말해주세요.\n취소하려면 아무 말이나 입력해 주세요.", color=random_color, timestamp=datetime.datetime.utcnow())
                    embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
                    mm = await message.channel.send(embed=embed)
                    
                    def check(m):
                        return m.author == message.author and m.channel == message.channel
                    
                    try:
                        msg = await client.wait_for('message', timeout=30.0, check=check)
                    except asyncio.TimeoutError:
                        embed = discord.Embed(title=":exclamation: **취소되었습니다.**", description="작업이 취소되었습니다.", color=red, timestamp=datetime.datetime.utcnow())
                        embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
                        await mm.edit(embed=embed)
                    else:
                        if len(msg.attachments) >= 1:
                            embed = discord.Embed(title=":white_check_mark: **패치노트 업로드 완료!**", description="올리신 패치노트는 <#620131472786980894>에 업로드되었습니다.", color=random_color, timestamp=datetime.datetime.utcnow())
                            embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
                            await mm.edit(embed=embed)
                            channel = client.get_channel(620131472786980894)
                            embed = discord.Embed(title=f":tools: **{title}**", description=f"{naeyong}", color=random_color, timestamp=datetime.datetime.utcnow())
                            embed.add_field(name="**사진 또는 동영상**", value="아래 첨부.", inline=True)
                            embed.set_image(url=msg.attachments[0].url)
                            embed.set_footer(text="for everyone", icon_url=client.user.avatar_url)
                            await channel.send(embed=embed)
                            await msg.delete()
                        elif msg.content == "아니오" or msg.content == "아니요":
                            embed = discord.Embed(title=":white_check_mark: **패치노트 업로드 완료!**", description="올리신 패치노트는 <#620131472786980894>에 업로드되었습니다.", color=random_color, timestamp=datetime.datetime.utcnow())
                            embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
                            await mm.edit(embed=embed, content="자료 없이 업로드됩니다.")
                            channel = client.get_channel(620131472786980894)
                            embed = discord.Embed(title=f":tools: **{title}**", description=f"{naeyong}", color=random_color, timestamp=datetime.datetime.utcnow())
                            embed.set_footer(text="for everyone", icon_url=client.user.avatar_url)
                            await channel.send(embed=embed)
                            await msg.delete()
                        else:
                            embed = discord.Embed(title=":exclamation: **취소되었습니다.**", description="작업이 취소되었습니다.", color=red, timestamp=datetime.datetime.utcnow())
                            embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
                            await mm.edit(embed=embed)
            else:
                embed = discord.Embed(title=":question: **명령어가 잘못되었습니다!**", description="패치노트 업로드 명령어는 ``/패치노트 (제목) (내용)``으로 사용합니다.\n*제목에서 띄어쓰려면 언더바(_)를 사용하세요. *(예: DAY_ZH)*", color=red, timestamp=datetime.datetime.utcnow())
                embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
                await message.channel.send(embed=embed)
        elif command == "공지":
            if not message.author.id in staff:
                embed = discord.Embed(title=":exclamation: **권한이 부족합니다.**", description="이 명령어는 관리자만 사용할 수 있습니다.", color=red, timestamp=datetime.datetime.utcnow())
                embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
                await message.channel.send(embed=embed)
                return
            if len(commandline.split()) >= 2:
                embed = discord.Embed(title=":white_check_mark: **공지 전송 완료!**", description="입력하신 내용은 <#622387695821520900>에 전송되었습니다.", color=random_color, timestamp=datetime.datetime.utcnow())
                embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
                await message.channel.send(embed=embed)
                channel = client.get_channel(622387695821520900)
                title = commandline.split()[0].replace("`","").replace("*","").replace("_"," ")
                naeyong = ' '.join(commandline.split()[1:])
                embed = discord.Embed(title=f":mega: **{title}**", description=f"{naeyong}", color=random_color, timestamp=datetime.datetime.utcnow())
                if len(message.attachments) >= 1:
                    embed.add_field(name="**사진 또는 동영상**", value="아래 첨부.", inline=True)
                    embed.set_image(url=message.attachments[0].url)
                embed.set_footer(text=f"sent by {message.author.name}", icon_url=message.author.avatar_url)
                await channel.send(embed=embed)
            else:
                embed = discord.Embed(title=":question: **명령어가 잘못되었습니다!**", description="공지 전송 명령어는 ``/공지 (제목) (내용)``으로 사용합니다.\n*제목에서 띄어쓰려면 언더바(_)를 사용하세요. *(예: DAY_ZH)*", color=red, timestamp=datetime.datetime.utcnow())
                embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
                await message.channel.send(embed=embed)
        elif command == "처벌":
            if not message.author.id in staff:
                embed = discord.Embed(title=":exclamation: **권한이 부족합니다.**", description="이 명령어는 관리자만 사용할 수 있습니다.", color=red, timestamp=datetime.datetime.utcnow())
                embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
                await message.channel.send(embed=embed)
                return
            if len(commandline.split()) >= 3:
                title = "유저 처벌"
                if commandline.split()[0] == "차단" or commandline.split()[0] == "밴":
                    chubul = 1
                    title = "차단"
                elif commandline.split()[0] == "추방" or commandline.split()[0] == "킥":
                    chubul = 2
                    title = "추방"
                elif commandline.split()[0] == "채팅정지" or commandline.split()[0] == "뮤트":
                    chubul = 3
                    title = "채팅 정지"
                elif commandline.split()[0] == "서버처벌":
                    chubul = 3
                    title = "서버 내 처벌"
                else:
                    embed = discord.Embed(title=":question: **명령어가 잘못되었습니다!**", description="처벌 명령어는 ``/처벌 (차단/추방/채팅정지/서버처벌) (유저맨션) (사유)``로 사용합니다.", color=red, timestamp=datetime.datetime.utcnow())
                    embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
                    await message.channel.send(embed=embed)
                    return
                if commandline.split()[1].startswith("<@"):
                    userid = commandline.split()[1].replace("<@","").replace(">","").replace("!","")
                    user = client.get_user(int(userid))
                    member = message.guild.get_member(int(userid))
                else:
                    channel = client.get_channel(634372847770402816)
                    reason = ' '.join(commandline.split()[2:]).replace("`","")
                    await message.channel.send(content=":ok_hand: 처벌 완료")
                    embed = discord.Embed(title=f":no_entry: **서버 내 처벌**", description=f"유저 한 명이 서버 내 처벌 처리되었습니다.", color=red, timestamp=datetime.datetime.utcnow())
                    embed.add_field(name="유저 인게임 이름:",value=f"{commandline.split()[1]}", inline=True)
                    embed.add_field(name="사유:",value=f"```{reason}```", inline=True)
                    embed.set_footer(text=f"sent by {message.author.name}", icon_url=message.author.avatar_url)
                    await channel.send(embed=embed)
                    return
                channel = client.get_channel(634372847770402816)
                reason = ' '.join(commandline.split()[2:]).replace("`","")
                await message.channel.send(content=":ok_hand: 처벌 완료")
                embed = discord.Embed(title=f":no_entry: **{title}**", description=f"유저 한 명이 {title} 처리되었습니다.", color=red, timestamp=datetime.datetime.utcnow())
                embed.add_field(name="유저:",value=f"{user.name} ({user.display_name}) [{str(user.id)}]", inline=True)
                embed.add_field(name="사유:",value=f"```{reason}```", inline=True)
                embed.set_footer(text=f"sent by {message.author.name}", icon_url=message.author.avatar_url)
                await channel.send(embed=embed)
                if chubul == 0:
                    embed = discord.Embed(title=f":no_entry: **{title}**", description=f"당신은 DayZH 서버에서 처벌되었습니다.\n이의 제기를 하려면 ``XxPKBxX#4684``에게 DM을 보내십시오.", color=red, timestamp=datetime.datetime.utcnow())
                    embed.add_field(name="처벌자:",value=f"{message.author.name} ({message.author.display_name})", inline=True)
                    embed.add_field(name="사유:",value=f"```{reason}```", inline=True)
                    embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
                    await user.send(embed=embed)
                else:
                    embed = discord.Embed(title=f":no_entry: **{title}**", description=f"당신은 DayZH에서 {title} 처리되었습니다.\n이의 제기를 하려면 ``XxPKBxX#4684``에게 DM을 보내십시오.", color=red, timestamp=datetime.datetime.utcnow())
                    embed.add_field(name="처벌자:",value=f"{message.author.name} ({message.author.display_name})", inline=True)
                    embed.add_field(name="사유:",value=f"```{reason}```", inline=True)
                    embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
                    await user.send(embed=embed)
                if chubul == 1:
                    await message.guild.ban(user, reason=reason)
                elif chubul == 2:
                    await message.guild.kick(user, reason=reason)
                elif chubul == 3:
                    role = message.guild.get_role(634977948746645544)
                    await member.add_roles(role, reason=reason)
            else:
                embed = discord.Embed(title=":question: **명령어가 잘못되었습니다!**", description="처벌 명령어는 ``/처벌 (차단/추방/채팅정지/서버처벌) (유저맨션) (사유)``로 사용합니다.", color=red, timestamp=datetime.datetime.utcnow())
                embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
                await message.channel.send(embed=embed)
        elif command == "단어검색" or command == "사전검색" or command == "단어사전" or command == "단어" or command == "표국대":
            if len(commandline.split()) == 1:
                searchWord = commandline.split()[0].replace("`","").replace("*","").replace("_","")
                api = f"https://stdict.korean.go.kr/api/search.do?certkey_no=982&key=key&type_search=search&q={searchWord}"
                try:
                    response = requests.get(api).text
                    jsonResponse = json.loads(json.dumps(xmltodict.parse(response)))
                except Exception as error:
                    embed = discord.Embed(title=":question: **앗! 나의 실수...**", description="표국대 단어 검색 결과를 불러오는 데 오류가 발생하였습니다.\n나중에 다시 시도해 주세요.\n오류 내용은 봇 제작자에게 전달되었습니다.", color=red, timestamp=datetime.datetime.utcnow())
                    embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
                    await message.channel.send(embed=embed)
                    pkb = client.get_user(278441794633465876)
                    embed = discord.Embed(title=":warning: 오류 발생!", description="표국대 단어 검색 결과를 불러오는 데 오류가 발생하였습니다.\n에러 내용을 아래에서 확인해 주세요.", color=red, timestamp=datetime.datetime.utcnow())
                    embed.add_field(name="오류 내용:", value=f"{error}", inline=True)
                    embed.add_field(name="명령어 내용:", value=f"{message.content}", inline=True)
                    embed.add_field(name="명령어 사용자:", value=f"{message.author} | {str(message.author.id)}", inline=True)
                    embed.set_footer(text=f"for {pkb.name}", icon_url=message.author.avatar_url)
                    await pkb.send(embed=embed)
                    return
                if int(jsonResponse["channel"]["total"]) >= 1:
                    embed = discord.Embed(title=":white_check_mark: **단어 검색 완료!**", description=f"입력하신 단어 ``{searchWord}``을(를) **표준국어대사전**에서 검색했습니다.\n아래에서 확인하세요.", color=random_color, timestamp=datetime.datetime.utcnow())
                    total = int(jsonResponse["channel"]["total"])
                    embed.add_field(name="총 검색된 단어 뜻 수:", value=f"{total}개", inline=True)
                    if total == 1:
                        item = jsonResponse["channel"]["item"]
                        pos = item["pos"]
                        defi = item["sense"]["definition"]
                        embed.add_field(name=f"1번째 뜻: ({pos})", value=f"{defi}", inline=True)
                    else:
                        for i in range(total):
                            item = jsonResponse["channel"]["item"][i]
                            pos = item["pos"]
                            defi = item["sense"]["definition"]
                            embed.add_field(name=f"{str(i + 1)}번째 뜻: ({pos})", value=f"{defi}", inline=True)
                    embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
                    await message.channel.send(embed=embed)
                else:
                    embed = discord.Embed(title=":exclamation: **단어 검색 실패...**", description=f"입력하신 단어 ``{searchWord}``은(는) **표준국어대사전**에 등재되어 있지 않습니다.\n다른 단어를 입력해 주세요.", color=red, timestamp=datetime.datetime.utcnow())
                    embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
                    await message.channel.send(embed=embed)
            else:
                embed = discord.Embed(title=":question: **명령어가 잘못되었습니다!**", description="단어 검색 명령어는 ``/단어검색 (단어)``로 사용합니다.\n*띄어쓰기는 허용되지 않습니다.", color=red, timestamp=datetime.datetime.utcnow())
                embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
                await message.channel.send(embed=embed)
        else:
            embed = discord.Embed(title=":question: **명령어가 잘못되었습니다!**", description="입력하신 명령어는 존재하지 않습니다.", color=red, timestamp=datetime.datetime.utcnow())
            embed.set_footer(text=f"for {message.author.name}", icon_url=message.author.avatar_url)
            await message.channel.send(embed=embed)

client.run(token)
