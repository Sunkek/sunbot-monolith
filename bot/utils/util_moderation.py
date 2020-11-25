from datetime import datetime

CREATE_MUTE = """INSERT INTO muted VALUES ($1, $2, now(), $3);"""
ADD_MUTE = """
UPDATE muted SET duration = duration + $1 WHERE guild_id = $2 AND user_id = $3;
"""
REMOVE_MUTE = """DELETE FROM muted WHERE guild_id = $1 AND user_id = $2;"""
FETCH_EXPIRED_MUTES = """
SELECT guild_id, user_id FROM muted 
WHERE start + interval '1h' * duration < $1
"""
DELETE_EXPIRED_MUTES = """
DELETE FROM muted 
WHERE start + interval '1h' * duration < $1
"""

from asyncpg.exceptions import ForeignKeyViolationError, UniqueViolationError

from utils import util_trackers

async def mute(bot, guild_id, member_id, hours: int):
    """Add the mute entry to the database for persistency"""
    try:
        async with bot.db.acquire() as connection:
            async with connection.transaction():
                await connection.execute(
                    CREATE_MUTE, guild_id, member_id, abs(hours),
                )
    except ForeignKeyViolationError:
        await util_trackers.create_missing_user(bot, member_id)
        await mute(bot, guild_id, member_id, hours)
    except UniqueViolationError:
        async with bot.db.acquire() as connection:
            async with connection.transaction():
                await connection.execute(
                    ADD_MUTE, hours, guild_id, member_id,
                )
                
async def unmute(bot, guild_id, member_id):
    """Remove the mute entry"""
    async with bot.db.acquire() as connection:
        async with connection.transaction():
            await connection.execute(
                REMOVE_MUTE, guild_id, member_id
            )

async def fetch_for_unmute(bot):
    """Fetch the expired mutes, and remove them from the DB"""
    async with bot.db.acquire() as connection:
        async with connection.transaction():
            now = datetime.now()
            res = await connection.fetch(FETCH_EXPIRED_MUTES, now)
            await connection.execute(DELETE_EXPIRED_MUTES, now)
            return [(i["guild_id"], i["user_id"]) for i in res]
