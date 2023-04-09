import sqlite3

# Create a connection to the database
conn = sqlite3.connect('prices.db')
c = conn.cursor()

# Create a table to store the prices
c.execute(
    'CREATE TABLE prices (website text, query text, item text, price real, time real, link text, search text)'
)
c.execute(
    'CREATE TABLE users (first_name text, user_id integer, last_name text, date_created real)'
)
c.execute(
    'CREATE TABLE usage (user_id integer, command text, date_received real)'
)


# Commit the changes and close the connection
conn.commit()
conn.close()