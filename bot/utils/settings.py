SELECT_TABLE_NAMES = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
CREATE_GUILDS_TABLE = """
CREATE TABLE IF NOT EXISTS guilds (
    guild_id bigint PRIMARY KEY
);"""
CREATE_TRACKERS_TABLE = """
CREATE TABLE IF NOT EXISTS trackers (
    guild_id bigint PRIMARY KEY REFERENCES guilds (guild_id),
    track_messages boolean DEFAULT 'false'
);"""

def format_setting(records):
    """Change a list of records into a dict of settings per guild id"""
    result = {i["guild_id"]: {
        k: v for k, v in i.items() if k != "guild_id"
    } for i in records}
    return result

async def read_settings(connection_pool):
    """Read bot settings from the database. 
    Create missing tables if there are any."""
    settings = dict()
    async with connection_pool.acquire() as connection:
        async with connection.transaction():
            # Create tables if they don't exist
            tables = await connection.fetch(SELECT_TABLE_NAMES)
            tables = [i["table_name"] for i in tables]
            if "guilds" not in tables:
                await connection.execute(CREATE_GUILDS_TABLE)
            if "trackers" not in tables:                    
                await connection.execute(CREATE_TRACKERS_TABLE)
            # Fetch the settings
            trackers = await connection.fetch("SELECT * FROM trackers")
            settings["trackers"] = format_setting(trackers)
    print(settings)
    return settings