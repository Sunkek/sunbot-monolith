async def change_user_info(bot, user_id, **kwargs):
    """Change user info in the database"""
    async with bot.db.acquire() as connection:
        async with connection.transaction():
            for k, v in kwargs.items():
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