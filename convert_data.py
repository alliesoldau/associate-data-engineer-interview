import json
import sqlite3

connection = sqlite3.connect('client_records.sqlite')
cursor = connection.cursor()
cursor.execute('Create Table if not exists ClientRecords (time_call_began datetime, time_call_ended datetime, counselors string, transfer_timestamps datetime, issues_discussed string, call_rating integer, initial_risk_level integer, client_pronouns string, client_name string, client_location string)')

# read through each line in the JSONL file and append it to the client_records array 
client_records = []
with open('client_records.json') as f:
    for line in f:
        client_records.append(json.loads(line))

# define columns 
columns_client_records = ['time_call_began','time_call_ended','counselors', 'transfer_timestamps','issues_discussed','call_rating','initial_risk_level','client_pronouns', 'client_name', 'client_location']
# loop through client_records and add data to our table 
for row in client_records:
    keys= tuple(row[c] for c in columns_client_records)
    cursor.execute('insert into ClientRecords values(?,?,?,?,?,?,?,?,?,?)', keys)
# TO DO: next I need to create my 3 different tables
# TO DO: add in an id column
# TO DO: parse data into its proper columns
connection.commit()
connection.close()