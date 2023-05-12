import json
import sqlite3

# create table for all raw data
connection = sqlite3.connect('client_records.sqlite')
cursor = connection.cursor()
# FOR RAW DATA FULL TABLE
# cursor.execute('Create Table if not exists ClientRecords (time_call_began datetime, time_call_ended datetime, counselors string, transfer_timestamps datetime, issues_discussed string, call_rating integer, initial_risk_level integer, client_pronouns string, client_name string, client_location string)')
cursor.execute('Create Table if not exists Counselors (id integer primary key, name string)')
cursor.execute('Create Table if not exists Contacts (id integer primary key, time_call_began datetime, time_call_ended datetime, issues_discussed string, call_rating integer, initial_risk_level integer, client_pronouns string, client_name string, client_location string, initial_counelor_id integer, total_transfers integer)')

# read through each line in the JSONL file and append it to the client_records array 
client_records = []
with open('client_records.json') as f:
    for line in f:
        client_records.append(json.loads(line))

# define columns 
# FOR RAW DATA FULL TABLE # columns_client_records = ['time_call_began','time_call_ended','counselors', 'transfer_timestamps', 'issues_discussed','call_rating','initial_risk_level','client_pronouns', 'client_name', 'client_location']
columns_counselors = ['counselors']
columns_contacts = ['time_call_began','time_call_ended', 'issues_discussed', 'call_rating', 'initial_risk_level', 'client_pronouns', 'client_name', 'client_location']
# loop through client_records and add data to our table 
# DRAW BACK: if 2 counselors have the same name there's no way to know if they're dulpicates or individuals. A unique counselor ID supplied by Trevor would help
uniqueNames = []
for row in client_records:
    # counselor data
    name = tuple(row[c] for c in columns_counselors)
    names = name[0].split(",")
    total_transfers = (len(names))
    # add unique counselors to the table
    currentName = []
    if len(names) > 0:
        counter = 0
        while counter < len(names):
            currentName = names[counter]
            # initializing bad_chars_list
            bad_chars = [';', ':', '!', "*", "[", "]", ",", '" ', ' "', '"', "'" ]
            # using replace() to remove bad_chars
            for i in bad_chars:
                currentName = currentName.replace(i, '')
            # update the unique names array if you find a novel name and add it to the table    
            if counter == 0:
                initial_counselor = currentName
            if currentName not in uniqueNames:
                uniqueNames.append(currentName)
                cursor.execute('insert into Counselors(name) values (?)', (currentName,))
            counter += 1
    # contacts data
    # TO DO: fix pronouns so that they don't have the quotes. if its an array we can use it easier
    # TO DO: fix other strings to remove quotes 
    contact = list(row[c] for c in columns_contacts)
    cursor.execute('SELECT id FROM Counselors WHERE name=?', (initial_counselor,))
    initial_counselor_tuple = cursor.fetchall()
    initial_counselor_id = initial_counselor_tuple[0]
    contact.append(initial_counselor_id[0])
    contact.append(total_transfers)
    cursor.execute('insert into Contacts(time_call_began, time_call_ended, issues_discussed, call_rating, initial_risk_level, client_pronouns, client_name, client_location, initial_counelor_id, total_transfers) values (?,?,?,?,?,?,?,?,?,?)', contact)

# TO DO: make transfer table
# TO DO: if value is empty have value be nil?
connection.commit()
connection.close()