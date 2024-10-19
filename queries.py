from db import get_connection, release_connection

#This function will execute a query and return the results. It is a generalized form to avoid repeating get_connection and release_connection in every query execution.
def execute_query(query):
    """Execute a database query and return the results."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        if cursor.description:  # Check if the query returns results
            return cursor.fetchall(), None
        else:
            conn.commit()  # Commit if it's an INSERT/UPDATE/DELETE query
            return None, None  # Return None for non-SELECT queries
    except Exception as e:
        print(f"Error executing query: {e}")
        return None, e
    finally:
        cursor.close()  # Always close the cursor
        release_connection(conn)  # Release the connection back to the pool


