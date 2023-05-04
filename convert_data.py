import json
import sqlite3

connection = sqlite3.connect('db.sqlite')
cursor = connection.cursor()
cursor.execute('Create Table if not exists ClientRecords (time_call_began datetime, time_call_ended datetime, counselors string, transfer_timestamps datetime, issues_discussed string, call_rating integer, initial_risk_level integer, client_pronouns string, client_name string, client_location string)')

client_records = []
with open('client_records.json') as f:
    for line in f:
        client_records.append(json.loads(line))
print(client_records[3])
columns = ['time_call_began','time_call_ended','counselors', 'transfer_timestamps','issues_discussed','call_rating','initial_risk_level','client_pronouns', 'client_name', 'client_location']
for row in client_records:
    keys= tuple(row[c] for c in columns)
    cursor.execute('insert into ClientRecords values(?,?,?,?,?,?,?,?,?,?)', keys)
    print(f'{row["name"]} data inserted Succefully')

connection.commit()
connection.close()