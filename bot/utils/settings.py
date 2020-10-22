async def read_settings(connection_pool):
    """Read bot settings from the database. 
    Create missing tables if there are any."""
    settings = dict()
    async with connection_pool.acquire() as connection:
        async with connection.transaction():
            # Fetch tracker settings
            try:
                result = await connection.fetch(
                    "SELECT * FROM trackers"
                )
            except Exception as e:
                print(e)
                print(type(e))
            print(result)

    return settings