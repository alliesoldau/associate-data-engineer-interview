import json
import sqlite3

# create table for all raw data
connection = sqlite3.connect('client_records.sqlite')
cursor = connection.cursor()
# FOR RAW DATA FULL TABLE
# cursor.execute('Create Table if not exists ClientRecords (time_call_began datetime, time_call_ended datetime, counselors string, transfer_timestamps datetime, issues_discussed string, call_rating integer, initial_risk_level integer, client_pronouns string, client_name string, client_location string)')
cursor.execute('Create Table if not exists Counselors (id integer primary key, name string)')
cursor.execute('Create Table if not exists Transfers (id integer primary key, contact_id integer, counselor_id integer, timestamp datetime)')

# read through each line in the JSONL file and append it to the client_records array 
client_records = []
with open('client_records.json') as f:
    for line in f:
        client_records.append(json.loads(line))

# define columns 
# FOR RAW DATA FULL TABLE # columns_client_records = ['time_call_began','time_call_ended','counselors', 'transfer_timestamps', 'issues_discussed','call_rating','initial_risk_level','client_pronouns', 'client_name', 'client_location']
column_client_records_counselor_name = ['counselors']
# loop through client_records and add data to our table 
# DRAW BACK: if 2 counselors have the same name there's no way to know if they're dulpicates or individuals. A unique counselor ID supplied by Trevor would help
uniqueNames = []
for row in client_records:
    # FOR RAW DATA FULL TABLE # value = tuple(row[c] for c in columns_client_records)
    name = tuple(row[c] for c in column_client_records_counselor_name)
    names = name[0].split(",")
    # namesArray = name[0].split(",")
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
            if currentName not in uniqueNames:
                uniqueNames.append(currentName)
                cursor.execute('insert into Counselors(name) values (?)', (currentName,))
            counter += 1
    # TO DO: clean the data now that you can grad individual items
    # NOTICE: arrays seem to always have quotes, what's up with that
    # FOR RAW DATA FULL TABLE # cursor.execute('insert into ClientRecords values (?,?,?,?,?,?,?,?,?,?)', value)


# TO DO: next I need to create my 3 different tables
# TO DO: if value is empty have value be nil?
# TO DO: parse data into its proper columns
connection.commit()
connection.close()