import json
import sqlite3
from datetime import datetime

# functions
bad_chars = ["[", "]", '" ', ' "', "' ", " '", '"', "'"]
bad_chars_no_space = ["[", "]", '"', "'"]
def clean_string(exclude, string):
    for i in exclude:
        string = string.replace(i, '')
    return string

# create and connect to database
connection = sqlite3.connect('client_records.sqlite')
cursor = connection.cursor()

# create tables
cursor.execute("""CREATE Table if not exists Counselors 
                    (
                        id integer primary key, 
                        name string
                    )
               """)
cursor.execute("""CREATE Table if not exists Contacts 
                    (
                        id integer primary key, 
                        time_call_began datetime, 
                        time_call_ended datetime, 
                        call_rating integer, 
                        initial_risk_level integer, 
                        client_name string, 
                        client_location string, 
                        client_pronouns string, 
                        issues_discussed string, 
                        initial_counselor_id integer, 
                        total_transfers integer
                    )
                """)
cursor.execute("""CREATE Table if not exists Transfers 
                    (
                        id integer primary key, 
                        contact_id integer, 
                        counselor_id integer, 
                        timestamp datetime
                    )
                """)
# define base columns for Contacts table to save time later on
columns_contacts = ['time_call_began','time_call_ended', 'call_rating', 'initial_risk_level', 'client_name', 'client_location']

# read through each line in the JSONL file and append it to the client_records array 
client_records = []
with open('client_records.json') as f:
    for line in f:
        client_records.append(json.loads(line))

# loop through client_records array and add data to our tables 
# checking for unique names helps us avoid duplicate counselors in the counselors table
uniqueNames = []
for row in client_records:
    # COUNSELORS TABLE DATA
    names = (tuple(row[c] for c in ['counselors']))[0].split(",")
    total_transfers = (len(names) - 1)
    # add unique counselors to the table
    currentName = []
    if len(names) > 0:
        counter = 0
        # counselor transfers keeps track of which counselor is associated with which transfer
        counselor_transfers = []
        while counter < len(names):
            currentName = names[counter]
            # clean names
            currentName = (clean_string(bad_chars, currentName))  
            if counter == 0:
                initial_counselor = currentName
            # append unique names if found
            if currentName not in uniqueNames:
                uniqueNames.append(currentName)
                cursor.execute('INSERT INTO Counselors(name) VALUES (?)', (currentName,))
            # append counselor transfers so we can keep track for the transfer table
            counselor_transfers.append(currentName)
            counter += 1

    # CONTACTS TABLE DATA
    # 1:1 transfer of data from the columns which share a name with the .json file
    contact = list(row[c] for c in columns_contacts)
    # grabbing pronouns independantly so I can clean the strings
    pronouns = (list(row[c] for c in ['client_pronouns'])[0])
    pronouns = clean_string(bad_chars_no_space, pronouns)
    contact.append(pronouns)
    # grabbing issues independantly so I can clean the strings
    issues = (list(row[c] for c in ['issues_discussed'])[0])
    issues = clean_string(bad_chars_no_space, issues)
    contact.append(issues)
    # grab the initial counselor's id. We have the initial counselor's name variable from when we made the counselor's table
    cursor.execute('SELECT id FROM Counselors WHERE name=?', (initial_counselor,))
    initial_counselor_id = ((cursor.fetchall())[0])[0]
    contact.append(initial_counselor_id)
    # total transfers was calculated above by the number of names
    contact.append(total_transfers)
    cursor.execute("""INSERT INTO Contacts
                        (
                            time_call_began, 
                            time_call_ended, 
                            call_rating, 
                            initial_risk_level, 
                            client_name, 
                            client_location, 
                            client_pronouns, 
                            issues_discussed, 
                            initial_counselor_id, 
                            total_transfers
                        ) 
                            VALUES (?,?,?,?,?,?,?,?,?,?)
                    """, contact)
    # grab the id for the contact row that we just inserted into the table for use in the transfer table below
    current_contact_id = cursor.lastrowid
    
    # TRANSFERS TABLE DATA
    # if no transfers we can skip this step
    if total_transfers > 0:
        timestamps = (tuple(row[c] for c in ['transfer_timestamps']))[0]
        timestamps = clean_string(bad_chars_no_space, timestamps)
        counter = 0
        # these pointers help us grab the proper timestamp since the timestamps are saved as strings
        pointer1 = 0;
        pointer2 = 19;
        # if there is more than one transfer the timestamps are strings and need to be parsed to convert to datetimes
        # if there is only one transfer the data is set up different. I convert them to arrays so that I can more easily parse them into datetimes
        if total_transfers > 1:
            while counter < total_transfers:
                transfer = [current_contact_id]
                # this utilizes the counselor_transfers array created earlier when inputting counselor names into the Counselors table
                cursor.execute('SELECT id FROM Counselors WHERE name=?', (counselor_transfers[counter + 1],))
                current_counselor_id = ((cursor.fetchall())[0])[0]
                transfer.append(current_counselor_id)
                if total_transfers == 1:
                    currentDateTimeArray = (timestamps[18:-1]).split(", ")
                    dateTimeFormatted = ('%s-0%s-0%s 0%s:%s:00' % (currentDateTimeArray[0], currentDateTimeArray[1], currentDateTimeArray[2], currentDateTimeArray[3], currentDateTimeArray[4]))
                    dateTime_obj = datetime.strptime(dateTimeFormatted, '%Y-%m-%d %H:%M:%S')
                else:
                    currentDateTime = timestamps[pointer1:pointer2]
                    dateTime_obj = datetime.strptime(currentDateTime, '%Y-%m-%d %H:%M:%S')
                transfer.append(dateTime_obj)
                cursor.execute("""INSERT INTO Transfers
                                    (
                                        contact_id, 
                                        counselor_id, 
                                        timestamp
                                    ) 
                                        VALUES (?,?,?)
                                """, transfer)
                pointer1 += 21
                pointer2 += 21
                counter += 1

connection.commit()
connection.close()