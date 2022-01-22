import psycopg2
# credentials kezeléshez
# Retrieve credentials.
from cryptography.fernet import Fernet
import os

# https://www.psycopg.org/docs/install.html#install-from-source

# credentials from encrypted key file:
# a key.key file a CreateCred.py -al készült
# https://www.geeksforgeeks.org/create-a-credential-file-using-python/
cred_filename = 'CredFile.ini'
key_file = 'key.key'
key = ''

with open('key.key', 'r') as key_in:
    key = key_in.read().encode()

# If you want the Cred file to be of one
# time use uncomment the below line
# os.remove(key_file)

f = Fernet(key)
with open(cred_filename, 'r') as cred_in:
    lines = cred_in.readlines()
    config = {}
    for line in lines:
        tuples = line.rstrip('\n').split('=', 1)
        if tuples[0] in ('Username', 'Password'):
            config[tuples[0]] = tuples[1]
    print(config)
    dbusername = config['Username']
    passwd = f.decrypt(config['Password'].encode()).decode()
    #print("Password:", passwd)

conn = psycopg2.connect(f"dbname=testdbhu user={dbusername} password={passwd}")



# Connect to your postgres DB
#conn = psycopg2.connect("dbname=test user=postgres")

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a query
cur.execute("SELECT * FROM parenttop")

# Retrieve query results
records = cur.fetchall()

print(records)
