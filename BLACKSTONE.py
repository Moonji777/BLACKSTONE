import discord
from discord.ext import commands
from discord import app_commands

intents = discord.Intents.all()  # 모든 인텐트 활성화
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user}로 로그인되었습니다.")
    try:
        synced = await bot.tree.sync()
        print(f"{len(synced)}개의 명령어가 동기화되었습니다.")
    except Exception as e:
        print(f"동기화 중 오류 발생: {e}")

@bot.event
async def on_member_join(member):
    # 신규 멤버에게 DM 전송
    try:
        welcome_message = """
# [ BLACKSTONE 안내 ] 
안녕하십니까, {0.display_name}님! 'BLACKSTONE'에 오신 것을 환영합니다.
저희 'BLACKSTONE'에서는 다음과 같은 방법으로 입사가 가능합니다.

    가. **서류 전형**
        서류 전형을 통해 합격된다면, 인턴 직급으로 회사에 성공적으로 입사가 됩니다.
        
    나. **면접 전형**
        면접 전형은, 각 부서에 채용할 경우 면접을 통해 사원으로 진급 및 해당 부서에 채용될 수 있습니다.

## [ BLACKSTONE 부서 종류]

가. 중앙행정국 - 'BLACKSTONE' 회사의 인사 외 주요 행정 업무를 담당합니다.
나. 안보지원국 - 'BLACKSTONE' 회사의 안전에 관련된 보안 업무를 담당합니다.

## [ BLACKSTONE 입사 안내]

귀하께서 'BLACKSTONE'의 입사를 희망한다면 다음 안내에 따라 행동해주시길 바랍니다.

1. <#1302083353918570519> 에서 서류 전형을 통해 입사하는 방법을 확인합니다.
2. 서류 전형으로 입사 방법을 확인 후, <#1302083389012312136> 에서 서류 전형을 지원하시길 바랍니다.
3. 대기 후, 서류 전형에서 합격이 된다면 'BLACKSTONE'에서의 다양한 경험이 가능합니다.
        
'BLACKSTONE'에서 행복한 시간이 되시길 바랍니다.
감사합니다.

BLACKSTONEㅣ어둠에 맞서 승리하라
        """
        await member.send(welcome_message.format(member))
        print(f'{member.display_name}에게 환영 메시지를 전송했습니다.')
    except discord.errors.Forbidden:
        print(f"{member.display_name}님에게 메시지를 보낼 수 없습니다. DM이 비활성화되어 있습니다.")

@bot.tree.command(name="dm", description="서버의 모든 사용자에게 DM을 보냅니다.")
@app_commands.describe(message="전송할 메시지 내용")
async def dm(interaction: discord.Interaction, message: str):
    # 특정 역할이 있는지 확인
    role_id = 1302205355685711933
    has_role = any(role.id == role_id for role in interaction.user.roles)

    if not has_role:
        await interaction.response.send_message("이 명령어를 사용하려면 관리 권한이 필요합니다.", ephemeral=True)
        return

    failed_users = []
    for member in interaction.guild.members:
        if not member.bot:  # 봇 제외
            try:
                await member.send(message)
                print(f"{member.display_name}에게 메시지를 전송했습니다.")
            except discord.Forbidden:
                failed_users.append(member.display_name)  # DM 비활성화된 사용자 저장

    # 결과 메시지
    if failed_users:
        await interaction.response.send_message(
            f"메시지를 전송했지만 일부 사용자에게 전송하지 못했습니다: {', '.join(failed_users)}", ephemeral=True
        )
    else:
        await interaction.response.send_message("모든 사용자에게 메시지를 성공적으로 전송했습니다.", ephemeral=True)

# 청소 명령어 추가 (/청소)
@bot.tree.command(name="청소", description="지정한 수의 메시지를 삭제합니다.")
@app_commands.describe(amount="삭제할 메시지 수")
async def clear(interaction: discord.Interaction, amount: int):
    # 특정 역할이 있는지 확인
    role_id = 1302205355685711933
    has_role = any(role.id == role_id for role in interaction.user.roles)

    if not has_role:
        await interaction.response.send_message("이 명령어를 사용하려면 특정 역할이 필요합니다.", ephemeral=True)
        return

    if amount < 1:
        await interaction.response.send_message("1 이상의 숫자를 입력하세요.", ephemeral=True)
        return
    deleted = await interaction.channel.purge(limit=amount)
    await interaction.response.send_message(f"{len(deleted)}개의 메시지를 삭제했습니다.", delete_after=5)


# 봇 실행 (봇 토큰 입력 필요)
bot.run('MTMwMTkyODY4MDkwNTI0ODg2OQ.GzC3Zm.7TEGDP-kzw70WvIOaP02XgU_4vLsq7fLHS86TQ')



