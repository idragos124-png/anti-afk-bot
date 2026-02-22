import discord
import asyncio

TOKEN = "MTQ3NTA1NDQ5ODkxNjYwMTkyOA.GUaU0r.n7WX3UYljlWBWQqCLRSMBXEcgD1zEst5LKWb5c"
AFK_TIME = 8 * 60  # 8 minute

intents = discord.Intents.default()
intents.members = True
intents.voice_states = True

bot = discord.Client(intents=intents)

afk_users = {}

@bot.event
async def on_voice_state_update(member, before, after):

    # Dacă intră în canalul AFK
    if after.channel and after.channel == member.guild.afk_channel:

        async def kick_after_delay():
            await asyncio.sleep(AFK_TIME)

            # Verificăm dacă încă este în AFK
            if member.voice and member.voice.channel == member.guild.afk_channel:
                if member.guild.me.top_role > member.top_role:
                    await member.kick(reason="AFK mai mult de 8 minute.")

        task = asyncio.create_task(kick_after_delay())
        afk_users[member.id] = task

    # Dacă iese din AFK
    if before.channel and before.channel == member.guild.afk_channel:
        if member.id in afk_users:
            afk_users[member.id].cancel()
            del afk_users[member.id]

bot.run("MTQ3NTA1NDQ5ODkxNjYwMTkyOA.GUaU0r.n7WX3UYljlWBWQqCLRSMBXEcgD1zEst5LKWb5c")