import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

import psycopg2
import random
import string

# Configurations
DB_NAME = "my_local_db"
USER = "postgres"
PASSWORD = "root"
HOST = "localhost"
PORT = "5432"

# Step 1: Connect to the default database
try:
    default_conn = psycopg2.connect(
        dbname="postgres", user=USER, password=PASSWORD, host=HOST, port=PORT
    )
    default_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    default_cursor = default_conn.cursor()

    # Step 2: Check if the database exists
    default_cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
    exists = default_cursor.fetchone()

    # Step 3: Create the database if it does not exist
    if not exists:
        print(f"Database '{DB_NAME}' does not exist. Creating...")
        default_cursor.execute(f"CREATE DATABASE {DB_NAME}")
    else:
        print(f"Database '{DB_NAME}' already exists.")

    default_cursor.close()
    default_conn.close()

except Exception as e:
    print(f"Error during DB check/creation: {e}")
    exit(1)

# Step 4: Connect to the new (or existing) database and create a sample table
try:
    db_conn = psycopg2.connect(
        dbname=DB_NAME, user=USER, password=PASSWORD, host=HOST, port=PORT
    )
    db_cursor = db_conn.cursor()

    # Create table if not exists
    db_cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        );
    """)

    db_cursor.execute(f"SELECT COUNT(*) FROM users;")
    item_count = db_cursor.fetchone()
    if item_count:
        item_count = item_count[0]
    else:
        item_count = 0
    print(f"Connected to the database and ensured 'users' table exists with {item_count} entries")
    db_conn.commit()
    db_cursor.close()
    db_conn.close()

except Exception as e:
    print(f"Error connecting to new database: {e}")


def insert_random_users(num_entries=100):
    """
    Connects to the PostgreSQL database and inserts a specified number of random user entries.

    Args:
        db_name (str): The name of the database.
        user (str): The database user.
        password (str): The password for the database user.
        host (str): The database host.
        port (str or int): The database port.
        num_entries (int, optional): The number of random user entries to insert. Defaults to 100.
    """
    try:
        db_conn = psycopg2.connect(
            dbname=DB_NAME, user=USER, password=PASSWORD, host=HOST, port=PORT
        )
        # db_conn = psycopg2.connect(
        #     dbname=db_name, user=user, password=password, host=host, port=port
        # )
        db_cursor = db_conn.cursor()

        for _ in range(num_entries):
            # Generate random name
            name_length = random.randint(5, 15)
            name = ''.join(random.choice(string.ascii_letters + ' ') for _ in range(name_length)).strip().title()

            # Generate random email
            email_prefix_length = random.randint(8, 12)
            email_prefix = ''.join(random.choice(string.ascii_lowercase) for _ in range(email_prefix_length))
            email_domain = random.choice(['gmail.com', 'yahoo.com', 'outlook.com', 'example.com'])
            email = f"{email_prefix}@{email_domain}"

            # Insert the random user data
            db_cursor.execute("""
                INSERT INTO users (name, email) VALUES (%s, %s);
            """, (name, email))

        db_conn.commit()
        print(f"Successfully inserted {num_entries} random user entries.")

    except psycopg2.Error as e:
        print(f"Error inserting data: {e}")

    finally:
        if db_cursor:
            db_cursor.close()
        if db_conn:
            db_conn.close()


#########################################

import psycopg2
import time

table_name = 'users'


def add_integer_column(column_name):
    """Adds an integer column to the specified table and logs the time taken."""
    start_time = time.time()
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, user=USER, password=PASSWORD, host=HOST, port=PORT
        )
        cursor = conn.cursor()

        alter_table_sql = f"ALTER TABLE {table_name} ADD COLUMN {column_name} INTEGER;"
        cursor.execute(alter_table_sql)
        conn.commit()

        end_time = time.time()
        duration = end_time - start_time
        print(
            f"Successfully added integer column '{column_name}' to table '{table_name}'. Time taken: {duration:.4f} seconds.")

    except psycopg2.Error as e:
        print(f"Error adding integer column: {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def add_string_column(column_name, length):
    """Adds an integer column to the specified table and logs the time taken."""
    start_time = time.time()
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, user=USER, password=PASSWORD, host=HOST, port=PORT
        )
        cursor = conn.cursor()

        alter_table_sql = f"ALTER TABLE {table_name} ADD COLUMN IF NOT EXISTS {column_name} VARCHAR({length});"
        cursor.execute(alter_table_sql)
        conn.commit()

        end_time = time.time()
        duration = end_time - start_time
        print(
            f"Successfully added string column '{column_name}' to table '{table_name}'. Time taken: {duration:.4f} seconds.")

    except psycopg2.Error as e:
        print(f"Error adding integer column: {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def change_column_type_to_string(column_name, string_length=100):
    """Changes the data type of the specified column to VARCHAR(string_length) and logs the time taken."""
    start_time = time.time()
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, user=USER, password=PASSWORD, host=HOST, port=PORT
        )
        cursor = conn.cursor()

        alter_table_sql = f"ALTER TABLE {table_name} ALTER COLUMN {column_name} TYPE VARCHAR({string_length});"
        cursor.execute(alter_table_sql)
        conn.commit()

        end_time = time.time()
        duration = end_time - start_time
        print(
            f"Successfully changed column '{column_name}' in table '{table_name}' to VARCHAR({string_length}). Time taken: {duration:.4f} seconds.")

    except psycopg2.Error as e:
        print(f"Error changing column type: {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def drop_column(column_name):
    """Changes the data type of the specified column to VARCHAR(string_length) and logs the time taken."""
    start_time = time.time()
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, user=USER, password=PASSWORD, host=HOST, port=PORT
        )
        cursor = conn.cursor()

        alter_table_sql = f"ALTER TABLE {table_name} DROP COLUMN IF EXISTS {column_name};"
        cursor.execute(alter_table_sql)
        conn.commit()

        end_time = time.time()
        duration = end_time - start_time
        print(
            f"Successfully dropped column '{column_name}' in table '{table_name}' . Time taken: {duration:.4f} seconds.")

    except psycopg2.Error as e:
        print(f"Error changing column type: {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def create_index(column_name, index_name=None):
    """Creates an index on the specified column of the table and logs the time taken."""
    start_time = time.time()
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME, user=USER, password=PASSWORD, host=HOST, port=PORT
        )
        cursor = conn.cursor()

        if index_name is None:
            index_name = f"idx_{table_name}_{column_name}"

        create_index_sql = f"CREATE INDEX IF NOT EXISTS {index_name} ON {table_name} ({column_name});"
        cursor.execute(create_index_sql)
        conn.commit()

        end_time = time.time()
        duration = end_time - start_time
        print(
            f"Successfully created index '{index_name}' on column '{column_name}' of table '{table_name}'. Time taken: {duration:.4f} seconds.")

    except psycopg2.Error as e:
        print(f"Error creating index: {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



# Example usage (replace with your actual database credentials and table/column names)

NEW_INT_COLUMN = "age"
EXISTING_COLUMN = "name"  # Example column to change type

# insert_random_users(5000000)

# # Add the integer column


# # Change the type of an existing column to string (VARCHAR(30))
# change_column_type_to_string(NEW_INT_COLUMN)
add_string_column("age", 15)
add_string_column("col1", 10)
add_string_column("col2", 150)
# add_string_column("col3", 50)
add_integer_column('col3')
create_index('col3', "col3_index")
change_column_type_to_string('col3', 100)
drop_column('col1')
drop_column('col2')
drop_column('col3')
