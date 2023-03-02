import sqlite3

# Create a connection to the database
conn = sqlite3.connect('prices.db')
c = conn.cursor()

c.execute(
    "Select datetime(time, 'unixepoch', 'localtime') time, count(*) from prices GROUp by time;"
)
for item in c:
    print(item)
c.execute("Select time, count(*) from prices GROUp by time;")
for item in c:
    print(item)

# Commit the changes and close the connection
conn.close()