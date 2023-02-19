import sqlite3
import fiyatlar
import time

# Create a connection to the database
conn = sqlite3.connect('prices.db')
c = conn.cursor()

 
# c.execute('INSERT INTO prices (website text, query text, item text, price real, time integer)')
prices = fiyatlar.main()
curr_time = time.time()
for website in prices:
    for item, price in prices[website].items():
        c.execute('INSERT INTO prices VALUES (?, ?, ?, ?, ?)', (website, item.split("@")[0].strip() , item, price, curr_time))

# Commit the changes and close the connection
conn.commit()
conn.close()