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

async def add_message(bot, **kwargs):
    async with bot.db.acquire() as connection:
        async with connection.transaction():
            res = await connection.execute(
                UPDATE_MESSAGES, 
                kwargs["postcount"], kwargs["attachments"], kwargs["words"], 
                kwargs["guild_id"], kwargs["channel_id"], kwargs["user_id"], 
                kwargs["period"], 
            )
            if " 0" in res:
                res = await connection.execute(
                    INSERT_MESSAGES,
                    kwargs["guild_id"], kwargs["channel_id"], kwargs["user_id"],
                    kwargs["postcount"], kwargs["attachments"], kwargs["words"], 
                    kwargs["period"],
                )

async def add_reaction(bot, **kwargs):
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
                    kwargs["guild_id"], kwargs["channel_id"], kwargs["giver_id"],
                    kwargs["receiver_id"], kwargs["emoji"], kwargs["count"], 
                    kwargs["period"],
                )
