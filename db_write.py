import sqlite3
import fiyatlar
import time

# Create a connection to the database
conn = sqlite3.connect('prices.db')
c = conn.cursor()

prices = fiyatlar.main()
curr_time = time.time()
for website in prices:
    for item, price in prices[website].items():
        if price == "":
            price = ["", "", ""]
        c.execute('INSERT INTO prices VALUES (?, ?, ?, ?, ?, ?, ?)',
                  (website, item.split("@")[0].strip(), item, price[0],
                   curr_time, price[1], price[2]))


# Commit the changes and close the connection
conn.commit()
conn.close()