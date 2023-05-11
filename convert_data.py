import json
import sqlite3

# create table for all raw data
connection = sqlite3.connect('client_records.sqlite')
cursor = connection.cursor()
cursor.execute('Create Table if not exists ClientRecords (time_call_began datetime, time_call_ended datetime, counselors string, transfer_timestamps datetime, issues_discussed string, call_rating integer, initial_risk_level integer, client_pronouns string, client_name string, client_location string)')
# create table for counselors
cursor.execute('Create Table if not exists Counselors (name string)')
# read through each line in the JSONL file and append it to the client_records array 
client_records = []
with open('client_records.json') as f:
    for line in f:
        client_records.append(json.loads(line))

# define columns 
columns_client_records = ['time_call_began','time_call_ended','counselors', 'transfer_timestamps', 'issues_discussed','call_rating','initial_risk_level','client_pronouns', 'client_name', 'client_location']
column_client_records_counselor_name = ['counselors']
# loop through client_records and add data to our table 
for row in client_records: # this will do it just for the first entry
# for row in client_records: # this will do it for all rows
    value = tuple(row[c] for c in columns_client_records)
    name = tuple(row[c] for c in column_client_records_counselor_name)
    names = name[0]
    namesArray = names.split(",")
    uniqueNames = []
    # this splits up any duplicate counselors and puts them into the counselors table independently
    if len(namesArray) > 1:
        counter = 0
        currentName = []
        while counter < len(namesArray):
            currentName = namesArray[counter]
            # initializing bad_chars_list
            bad_chars = [';', ':', '!', "*", "[", "]", ",", '" ', ' "', '"']
            # using replace() to remove bad_chars
            for i in bad_chars:
                currentName = currentName.replace(i, '')
            # update the unique names array if you find a novel name and add it to the table    
            if currentName not in uniqueNames:
                uniqueNames.append(currentName)
                cursor.execute('insert into Counselors values (?)', (currentName,))
            counter += 1
    # string literals should be single quotes not double qoutes (https://www.sqlite.org/quirks.html point 8)
    # TO DO: clean the data now that you can grad individual items
    # TO DO: ^^ see example above for how to grad just timestamp, then figure out how to manipulate it
    # NOTICE: arrays seem to always have quotes, what's up with that
    print(uniqueNames)
    cursor.execute('insert into ClientRecords values (?,?,?,?,?,?,?,?,?,?)', value)


# TO DO: next I need to create my 3 different tables
# TO DO: if value is empty have value be nil?
# TO DO: add in an id column
# TO DO: parse data into its proper columns
connection.commit()
connection.close()