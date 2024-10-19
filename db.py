# db.py

from psycopg2 import pool

# Initialize the connection pool globally
db_pool = None

# Initialize the connection pool
def init_db_pool(host, port, dbname, dbUser, dbPassword):
    global db_pool

    db_pool = pool.SimpleConnectionPool(
        minconn=1,  # Minimum number of connections
        maxconn=10,  # Maximum number of connections
        host=host,
        port=port,
        dbname=dbname,
        user=dbUser,
        password=dbPassword

    )

# Get a connection from the pool
def get_connection():
    """Get a connection from the pool."""
    return db_pool.getconn()

# Release a connection back to the pool
def release_connection(conn):
    """Release a connection back to the pool."""
    db_pool.putconn(conn)
