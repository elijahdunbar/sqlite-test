import sqlite3
import re

# create sqlite db called emaildb and link to it
conn = sqlite3.connect("emaildb.sqlite")
# create a cursor that allows us to use SQL commands
cur = conn.cursor()

# this is how to call SQL commands on the emaildb
cur.execute("DROP TABLE IF EXISTS Counts")

cur.execute("""
CREATE TABLE Counts (org TEXT, count INTEGER)""")

fname = input("Enter file name: ")
if len(fname) < 1:
    fname = "mbox.txt"
fh = open(fname)
for line in fh:
    if not line.startswith("From: "):
        continue
    pieces = line.split()
    email = pieces[1]
    # search emails for their domain names
    org = re.findall("@([a-z\S]+)", email)[0]
    # print(org)
    # print(email)
    # select in the db all rows where org = the domain name we got above
    cur.execute("SELECT count FROM Counts WHERE org = ? ", (org,))
    # this fetches one of the rows found
    row = cur.fetchone()
    # now we check if we even got a row and if we didn't, add it to the db
    if row is None:
        cur.execute(
            """INSERT INTO Counts (org, count)
                VALUES (?, 1)""",
            (org,),
        )
    else:
        # if we did find a row with the domain name, we add one to the count field and update the db
        cur.execute("UPDATE Counts SET count = count + 1 WHERE org = ?", (org,))
    # executes all the previous SQL commands
    conn.commit()

# select the top 10 occurences
sqlstr = "SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10"

# print them out
for row in cur.execute(sqlstr):
    print(str(row[0]), row[1])

cur.close()
