from quart_db import Connection

async def migrate(connection: Connection) -> None:
    await connection.execute("""
        CREATE TABLE Product (
            id INTEGER PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            quantity INTEGER DEFAULT 0,
            price FLOAT DEFAULT 0.0
        );

        CREATE TABLE User (
            id INTEGER PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(100) NOT NULL
        );""",
    )
    pass

async def valid_migration(connection: Connection) -> bool:
    return True