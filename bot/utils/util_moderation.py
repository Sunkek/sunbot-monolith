CREATE_MUTE = """INSERT INTO TABLE muted VALUES ($1, $2, now(), $3);"""
ADD_MUTE = """
UPDATE muted SET duration = duration + $1 WHERE guild_id = $2 AND user_id = $3;
"""
REMOVE_MUTE = """DELETE FROM muted WHERE guild_id = $1 AND user_id = $2;"""
REMOVE_MUTES_IF_ALLOWED = """
DELETE FROM muted WHERE start + interval '1h' * duration < now()
"""

async def mute(bot, guild_id, member_id, hours: int):
    """Add the mute entry to the database for persistency"""
    try:
        async with bot.db.acquire() as connection:
            async with connection.transaction():
                await connection.execute(
                    CREATE_MUTE, guild_id, member_id, abs(hours),
                )
    except Exception as e:
        print(e)
        print(type(e))
                
async def unmute_forced(bot, guild_id, member_id):
    """Remove the mute entry - if the mute is over"""
    async with bot.db.acquire() as connection:
        async with connection.transaction():
            await connection.execute(
                REMOVE_MUTE, guild_id, member_id
            )

async def unmute_by_time(bot):
    """Remove the mute entry - if the mute is over"""
    async with bot.db.acquire() as connection:
        async with connection.transaction():
            await connection.execute(
                REMOVE_MUTES_IF_ALLOWED
            )