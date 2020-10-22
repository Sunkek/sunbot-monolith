from asyncpg.exceptions import UndefinedTableError

async def read_settings(connection_pool):
    """Read bot settings from the database. 
    Create missing tables if there are any."""
    settings = dict()
    try:
        async with connection_pool.acquire() as connection:
            async with connection.transaction():
                # Create tables if they don't exist
                tables = await connection.fetch(
                    "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
                )
                if "guilds" not in tables:
                    await connection.execute(
                        "CREATE TABLE guilds ("
                            "guild_id bigint PRIMARY KEY"
                        ")"
                    )
                if "trackers" not in tables:                    
                    await connection.execute(
                        "CREATE TABLE trackers ("
                            "guild_id bigint PRIMARY KEY REFERENCES guilds (guild_id),"
                            "track_messages boolean DEFAULT 'false'"
                        ")"
                    )
                # Fetch the settings
                result = await connection.fetch(
                    "SELECT * FROM trackers"
                )
                print(result)
    except Exception as e:
        print(e)
        print(type(e))

    return settings