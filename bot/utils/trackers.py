UPDATE_MESSAGES = """
UPDATE messages 
SET postcount = postcount + $1, attachments = attachments + $2, words = words + $3
WHERE guild_id = $4 AND channel_id = $5 AND user_id = $6 AND period = $7;
"""
INSERT_MESSAGES = """
INSERT INTO messages 
VALUES ($1, $2, $3, $4, $5, $6, $7,);
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
            print(res)
            if " 0" in res:
                res = await connection.execute(
                    INSERT_MESSAGES,
                    kwargs["guild_id"], kwargs["channel_id"], kwargs["user_id"],
                    kwargs["postcount"], kwargs["attachments"], kwargs["words"], 
                    kwargs["period"],
                )
                print(res)