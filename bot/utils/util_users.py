FETCH_ELIGIBLE_USERS = """
SELECT user_id FROM activity
WHERE guild_id = $1 AND period + interval $2d > NOW()
GROUP BY user_id
HAVING AVG(from_text+from_attachments+from_reactions+from_voice) > $3
"""


async def change_user_info(bot, user_id, **kwargs):
    """Change user info in the database"""
    async with bot.db.acquire() as connection:
        async with connection.transaction():
            for k, v in kwargs.items():
                print(k, v)
                res = await connection.execute(
                    # TODO Editing the query string is dangerous, check later
                    f"UPDATE users SET {k} = $1 WHERE user_id = $2;", 
                    v, user_id
                )
                if " 0" in res:
                    await connection.execute(
                    # TODO Editing the query string is dangerous, check later
                    f"INSERT INTO users(user_id, {k}) VALUES ($1, $2);", 
                    user_id, v
                )

async def fetch_users_avg_activity(bot, guild_id, days, req_activity):
    async with bot.db.acquire() as connection:
        async with connection.transaction():
            print(days)
            res = await connection.fetch(
                FETCH_ELIGIBLE_USERS, guild_id, str(days), req_activity
            )
            return [i["user_id"] for i in res]
