CREATE_USER = """
INSERT INTO users
VALUES ($1)
"""
UPDATE_MESSAGES = """
UPDATE messages 
SET postcount = postcount + $1, attachments = attachments + $2, words = words + $3
WHERE guild_id = $4 AND channel_id = $5 AND user_id = $6 AND period = $7;
"""
INSERT_MESSAGES = """
INSERT INTO messages 
VALUES ($1, $2, $3, $4, $5, $6, $7);
"""
UPDATE_REACTIONS = """
UPDATE reactions 
SET count = count + $1
WHERE guild_id = $2 AND channel_id = $3 AND giver_id = $4 AND receiver_id = $5
AND emoji = $6 AND period = $7;
"""
INSERT_REACTIONS = """
INSERT INTO reactions 
VALUES ($1, $2, $3, $4, $5, $6, $7);
"""
UPDATE_VOICE = """
UPDATE voice 
SET count = count + $1
WHERE guild_id = $2 AND channel_id = $3 AND user_id = $4 AND members = $5 AND period = $6;
"""
INSERT_VOICE = """
INSERT INTO voice 
VALUES ($1, $2, $3, $4, $5, $6);
"""
UPDATE_GAMES = """
UPDATE games 
SET duration = duration + $1
WHERE user_id = $2 AND game = $3 AND period = $4;
"""
INSERT_GAMES = """
INSERT INTO games 
VALUES ($1, $2, $3, $4);
"""
from datetime import datetime, timedelta

from asyncpg.exceptions import ForeignKeyViolationError, UniqueViolationError

async def create_missing_user(bot, user_id):
    async with bot.db.acquire() as connection:
        async with connection.transaction():
            await connection.execute(CREATE_USER, user_id)

async def add_message(bot, **kwargs):
    try:
        async with bot.db.acquire() as connection:
            async with connection.transaction():
                res = await connection.execute(
                    UPDATE_MESSAGES, 
                    kwargs["postcount"], kwargs["attachments"], kwargs["words"], 
                    kwargs["guild_id"], kwargs["channel_id"], kwargs["user_id"], 
                    kwargs["period"], 
                )
                if " 0" in res:
                    await connection.execute(
                        INSERT_MESSAGES,
                        kwargs["guild_id"], kwargs["channel_id"], 
                        kwargs["user_id"], kwargs["postcount"], 
                        kwargs["attachments"], kwargs["words"], 
                        kwargs["period"],
                    )
    except ForeignKeyViolationError:
        # Create user if it doesn't exist
        await create_missing_user(bot, kwargs["user_id"])
        await add_message(bot, **kwargs)


async def add_reaction(bot, **kwargs):
    try:
        async with bot.db.acquire() as connection:
            async with connection.transaction():
                res = await connection.execute(
                    UPDATE_REACTIONS, 
                    kwargs["count"], kwargs["guild_id"], kwargs["channel_id"], 
                    kwargs["giver_id"], kwargs["receiver_id"], kwargs["emoji"], 
                    kwargs["period"], 
                )
                if " 0" in res:
                    res = await connection.execute(
                        INSERT_REACTIONS,
                        kwargs["guild_id"], kwargs["channel_id"], 
                        kwargs["giver_id"], kwargs["receiver_id"], 
                        kwargs["emoji"], kwargs["count"], kwargs["period"],
                    )
    except ForeignKeyViolationError:
        # Create users if they don't exist
        try:
            await create_missing_user(bot, kwargs["giver_id"])
        except UniqueViolationError:
            pass
        try:
            await create_missing_user(bot, kwargs["receiver_id"])
        except UniqueViolationError:
            pass
        await add_reaction(bot, **kwargs)


async def add_voice(bot, **kwargs):
    try:
        async with bot.db.acquire() as connection:
            async with connection.transaction():
                res = await connection.execute(
                    UPDATE_VOICE, 
                    kwargs["count"], kwargs["guild_id"], kwargs["channel_id"], 
                    kwargs["user_id"], kwargs["members"], kwargs["period"], 
                )
                if " 0" in res:
                    res = await connection.execute(
                        INSERT_VOICE,
                        kwargs["guild_id"], kwargs["channel_id"], 
                        kwargs["user_id"], kwargs["members"], kwargs["count"], 
                        kwargs["period"],
                    )
    except ForeignKeyViolationError:
        # Create user if it doesn't exist
        await create_missing_user(bot, kwargs["user_id"])
        await add_voice(bot, **kwargs)
    

async def add_game(bot, **kwargs):
    try:
        async with bot.db.acquire() as connection:
            async with connection.transaction():
                res = await connection.execute(
                    UPDATE_GAMES, 
                    kwargs["duration"], kwargs["user_id"], 
                    kwargs["game"], kwargs["period"], 
                )
                if " 0" in res:
                    res = await connection.execute(
                        INSERT_GAMES,
                        kwargs["user_id"], kwargs["game"], 
                        kwargs["duration"], kwargs["period"], 
                    )
    except ForeignKeyViolationError:
        # Create user if it doesn't exist
        await create_missing_user(bot, kwargs["user_id"])
        await add_game(bot, **kwargs)

async def add_activity(bot, guild_id, channel_id, user_id, period, **kwargs):
    print(kwargs)
    async with bot.db.acquire() as connection:
        async with connection.transaction():
            # Check activity cooldown
            cooldown = bot.settings.get(guild_id, {})\
                .get("activity_cooldown", 0) 
            print(cooldown)
            ok = datetime.now() > bot.last_active.get(guild_id, {})\
                .get(user_id, datetime(2000, 1, 1)) + timedelta(seconds=cooldown)
            print(datetime.now())
            print(bot.last_active.get(guild_id, {}).get(user_id, datetime(2000, 1, 1)))
            if not ok:
                return
            # Fetch channel multiplier
            channels_x0 = bot.settings.get(guild_id, {})\
                .get("activity_channels_x0", []) 
            channels_x05 = bot.settings.get(guild_id, {})\
                .get("activity_channels_x05", []) 
            channels_x2 = bot.settings.get(guild_id, {})\
                .get("activity_channels_x2", []) 
            multi = 1
            if channel_id in channels_x0:
                return
            elif channel_id in channels_x05:
                multi = 0.5
            elif channel_id in channels_x2:
                multi = 2

            for k, v in kwargs.items():
                if v:
                    res = await connection.execute(
                        # TODO Editing the query string is dangerous, check later
                        (f"UPDATE activity SET {k} = $1 "
                        "WHERE guild_id = $2 AND user_id = $3 AND period = $4;"), 
                        multi*v, guild_id, user_id, period
                    )
                    if " 0" in res:
                        await connection.execute(
                        # TODO Editing the query string is dangerous, check later
                        (f"INSERT INTO activity(guild_id, user_id, period, {k}) "
                        "VALUES ($1, $2, $3, $4);"), 
                        guild_id, user_id, period, multi*v
                    )
                    bot.last_active[guild_id][user_id] = datetime.now()
            # For cooldown
