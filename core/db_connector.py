import sqlite3

class DBConnector:
    def __init__(self, db_file):
        """
        Initializes the DBConnector.
        :param db_file: Path to the SQLite database file.
        """
        self.db_file = db_file
        self.connection = None

    def connect(self):
        """Establishes a connection to the database."""
        try:
            # `check_same_thread=False` is needed for Streamlit.
            self.connection = sqlite3.connect(self.db_file, check_same_thread=False)
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            self.connection = None

    def close(self):
        """Closes the database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None

    def execute_query(self, query, params=None):
        """
        Executes a given SQL query and returns the fetched results.
        Suitable for SELECT statements.
        """
        if not self.connection:
            print("Database connection is not established.")
            return None, None
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or [])
            # For SELECT queries, description will be set. For others, it's None.
            if cursor.description:
                columns = [description[0] for description in cursor.description]
                return cursor.fetchall(), columns
            else:
                self.connection.commit() # Commit changes for INSERT, UPDATE, DELETE
                return [], None # Return empty result for non-SELECT queries
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            return None, None

    def get_schema(self):
        """
        Retrieves the database schema as a descriptive string for the LLM.
        """
        if not self.connection:
            print("Database connection is not established.")
            return None
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            schema_str = "Database Schema:\n"
            for table_name_tuple in tables:
                table_name = table_name_tuple[0]
                schema_str += f"Table `{table_name}` has columns: "
                cursor.execute(f"PRAGMA table_info({table_name});")
                columns = cursor.fetchall()
                column_names = [col[1] for col in columns]
                schema_str += ", ".join(column_names) + ".\n"
            return schema_str
        except sqlite3.Error as e:
            print(f"Error retrieving schema: {e}")
            return None