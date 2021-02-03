from datetime import datetime, timedelta

FETCH_ELIGIBLE_USERS = """
SELECT user_id, SUM(from_text+from_attachments+from_reactions+from_voice)/$2 as avg_activity FROM activity
WHERE guild_id = $1 AND period + $2 * interval '1 day' > NOW()
GROUP BY user_id
HAVING SUM(from_text+from_attachments+from_reactions+from_voice)/$2 > $3
ORDER BY avg_activity DESC
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

async def fetch_users_by_days_and_activity(bot, guild, days, req_activity):
    async with bot.db.acquire() as connection:
        async with connection.transaction():
            res = await connection.fetch(
                FETCH_ELIGIBLE_USERS, guild.id, days, req_activity
            )
            active_users = [(i["user_id"], i["avg_activity"]) for i in res]
    pass_by_join_date = [
        m.id for m in guild.members 
        if m.joined_at + timedelta(days=days) < datetime.now() 
    ]
    return [i for i in active_users if i[0] in pass_by_join_date]