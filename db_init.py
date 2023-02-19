import sqlite3

# Create a connection to the database
conn = sqlite3.connect('prices.db')
c = conn.cursor()

# Create a table to store the prices
c.execute(
    'CREATE TABLE prices (website text, query text, item text, price real, time real)'
)

# Commit the changes and close the connection
conn.commit()
conn.close()