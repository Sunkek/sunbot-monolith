UPDATE_MESSAGES = """
UPDATE messages 
SET postcount = postcount + $, attachments = attachments + $, words = words + $
WHERE guild_id = $ AND channel_id = $ AND user_id = $ AND period = $;
"""
INSERT_MESSAGES = """
INSERT INTO messages 
VALUES ($, $, $, $, $, $, $,);
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