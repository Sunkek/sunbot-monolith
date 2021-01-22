FETCH_AVERAGE_ACTIVITY = """
SELECT SUM(from_text+from_attachments+from_reactions+from_voice)/$3
FROM activity
WHERE guild_id = $1 AND user_id = $2 AND period + $3 * interval '1 day' > NOW()
"""

async def fetch_average_activity(bot, guild_id, user_id, days_back=30):
    """Fetch user's average activity for the last N days"""
    async with bot.db.acquire() as connection:
        async with connection.transaction():
            return await connection.fetchval(
                FETCH_AVERAGE_ACTIVITY, guild_id, user_id, days_back
            )