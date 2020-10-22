from asyncpg.exceptions import UndefinedTableError

async def read_settings(connection_pool):
    """Read bot settings from the database. 
    Create missing tables if there are any."""
    settings = dict()
    async with connection_pool.acquire() as connection:
        async with connection.transaction():
            print(await connection.execute("\dt"))
            # Fetch tracker settings
            try:
                result = await connection.fetch(
                    "SELECT * FROM trackers"
                )
            except UndefinedTableError:
                await connection.execute(
                    """CREATE TABLE trackers (
                        guild_id biginteger PRIMARY KEY REFERENCES guilds (guild_id)
                    )"""
                )
                result = {}
            print(result)

    return settings