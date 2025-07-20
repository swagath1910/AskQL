import sqlite3
import os

# Define the path for the database
DB_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
DB_PATH = os.path.join(DB_DIR, 'sample_database.db')

# Create the data directory if it doesn't exist
os.makedirs(DB_DIR, exist_ok=True)

# Connect to the SQLite database (it will be created if it doesn't exist)
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Drop tables if they already exist to start fresh
cursor.execute("DROP TABLE IF EXISTS employees")
cursor.execute("DROP TABLE IF EXISTS departments")

# Create departments table
cursor.execute('''
CREATE TABLE departments (
    department_id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_name TEXT NOT NULL
)
''')

# Create employees table
cursor.execute('''
CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    position TEXT NOT NULL,
    hire_date DATE,
    salary INTEGER,
    department_id INTEGER,
    FOREIGN KEY (department_id) REFERENCES departments (department_id)
)
''')

# Insert sample data into departments
departments_data = [
    ('Engineering',),
    ('Human Resources',),
    ('Sales',),
    ('Marketing',)
]
cursor.executemany("INSERT INTO departments (department_name) VALUES (?)", departments_data)

# Insert sample data into employees
employees_data = [
    ('Alice Johnson', 'Software Engineer', '2020-01-15', 90000, 1),
    ('Bob Smith', 'HR Manager', '2019-03-10', 75000, 2),
    ('Charlie Brown', 'Sales Associate', '2021-07-21', 60000, 3),
    ('Diana Prince', 'Marketing Head', '2018-11-01', 110000, 4),
    ('Ethan Hunt', 'Senior Engineer', '2017-05-30', 120000, 1),
    ('Fiona Glenanne', 'Sales Director', '2019-08-15', 130000, 3)
]
cursor.executemany("INSERT INTO employees (name, position, hire_date, salary, department_id) VALUES (?, ?, ?, ?, ?)", employees_data)

// ...existing code...
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


# Commit the changes and close the connection
conn.commit()
conn.close()

print(f"Database '{os.path.basename(DB_PATH)}' created and populated successfully at '{DB_PATH}'")
