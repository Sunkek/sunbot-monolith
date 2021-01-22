from datetime import datetime, timedelta

FETCH_ELIGIBLE_USERS = """
SELECT user_id FROM activity
WHERE guild_id = $1 AND period + $2 * interval '1 day' > NOW()
GROUP BY user_id
HAVING SUM(from_text+from_attachments+from_reactions+from_voice)/$2 > $3
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
    try:
        async with bot.db.acquire() as connection:
            async with connection.transaction():
                res = await connection.fetch(
                    FETCH_ELIGIBLE_USERS, guild.id, days, req_activity
                )
                active_users = [i["user_id"] for i in res]
                print(active_users)
        for m in guild.members:
            print(m.joined_at + timedelta(days=days))
            print(m.joined_at + timedelta(days=days) < datetime.now())
            print(m.id in active_users)
        return [
            m for m in guild.members 
            if m.joined_at + timedelta(days=days) < datetime.now()
            and m.id in active_users
        ]
    except Exception as e:
        print(e)