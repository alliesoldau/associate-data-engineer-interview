import json
import sqlite3

# create database
connection = sqlite3.connect('client_records.sqlite')
cursor = connection.cursor()

cursor.execute('Create Table if not exists Counselors (id integer primary key, name string)')
cursor.execute('Create Table if not exists Contacts (id integer primary key, time_call_began datetime, time_call_ended datetime, call_rating integer, initial_risk_level integer, client_name string, client_location string, client_pronouns string, issues_discussed string, initial_counelor_id integer, total_transfers integer)')

# read through each line in the JSONL file and append it to the client_records array 
client_records = []
with open('client_records.json') as f:
    for line in f:
        client_records.append(json.loads(line))

# define columns 
columns_contacts = ['time_call_began','time_call_ended', 'call_rating', 'initial_risk_level', 'client_name', 'client_location']

# loop through client_records and add data to our table 
# DRAW BACK: if 2 counselors have the same name there's no way to know if they're dulpicates or individuals. A unique counselor ID supplied by Trevor would help
uniqueNames = []
for row in client_records:
    # counselor data
    name = tuple(row[c] for c in ['counselors'])
    names = name[0].split(",")
    total_transfers = (len(names))
    # add unique counselors to the table
    currentName = []
    if len(names) > 0:
        counter = 0
        while counter < len(names):
            currentName = names[counter]
            # initializing bad_chars_list
            bad_chars = ["[", "]", '"', "'", " "]
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
    pronoun = list(row[c] for c in ['client_pronouns'])
    pronouns = pronoun[0]
    # using replace() to remove bad_chars
    bad_chars_no_space = ["[", "]", '"', "'"]
    for i in bad_chars_no_space:
        pronouns = pronouns.replace(i, '')
    contact.append(pronouns)

    issue = list(row[c] for c in ['issues_discussed'])
    issues = issue[0]
    # using replace() to remove bad_chars
    for i in bad_chars_no_space:
        issues = issues.replace(i, '')
    contact.append(issues)
    cursor.execute('SELECT id FROM Counselors WHERE name=?', (initial_counselor,))
    initial_counselor_tuple = cursor.fetchall()
    initial_counselor_id = initial_counselor_tuple[0]
    # append in the columns I added (initial_counselor_id and total_transfers)
    contact.append(initial_counselor_id[0])
    contact.append(total_transfers)

    cursor.execute('insert into Contacts(time_call_began, time_call_ended, call_rating, initial_risk_level, client_name, client_location, client_pronouns, issues_discussed, initial_counelor_id, total_transfers) values (?,?,?,?,?,?,?,?,?,?)', contact)

# TO DO: make transfer table
# TO DO: if value is empty have value be nil?
connection.commit()
connection.close()