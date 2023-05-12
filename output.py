import sqlite3
connection = sqlite3.connect('client_records.sqlite')
cursor = connection.cursor()
# 1. Create an output csv with the data schema:
#        * | COUNSELOR NAME  | DAY  | NUMBER OF CASES  | AVERAGE RISK LEVEL  | AVERAGE RATING  |
cursor.execute('Create Table if not exists Output (COUNSELOR_NAME string, DAY date, NUMBER_OF_CASES integer, AVERAGE_RISK_LEVEL integer, AVERAGE_RATING integer)')
cursor.execute('SELECT name FROM Counselors')
names = ((cursor.fetchall()))
counter = 0
while counter < len(names):
    # grab the counselors name
    output_data = [names[counter][0]]
    # grab the distinct dates - in this case there's only one date but I grabbed it programmatically none the less
    cursor.execute('SELECT DISTINCT DATE(time_call_began) from Contacts')
    date = ((cursor.fetchall())[0])[0]
    output_data.append(date) 
    # grab the counselor's id so that we can get the number of cases
    cursor.execute('SELECT id FROM Counselors WHERE name=?', [names[counter][0]])
    counselor_id = ((cursor.fetchall())[0])[0]
    cursor.execute('SELECT COUNT(*) FROM Contacts WHERE initial_counselor_id=?', (counselor_id,))
    number_of_cases = ((cursor.fetchall())[0])[0]
    # we also need to add in the number of transfers, if we're assuming a case counts even if it wasn't theirs originally
    cursor.execute('SELECT COUNT(*) FROM Transfers WHERE counselor_id=?', (counselor_id,))
    number_of_transfers = ((cursor.fetchall())[0])[0]
    total_cases_with_transfers = number_of_cases + number_of_transfers
    output_data.append(total_cases_with_transfers)
    # find the average risk level for original cases and transfers
    # cursor.execute('SELECT AVG(*) FROM Contacts WHERE initial_counselor_id=?', (counselor_id,))
    cursor.execute('insert into Output(COUNSELOR_NAME, DAY, NUMBER_OF_CASES) values (?,?,?)', output_data,)
    counter += 1


# 2. The maximum number of concurrent cases handled by trevor at any time
# 3. A list of counselors who dealt with more than one concurrent cases
# 4. The average risk level of people who use `She/They` pronouns
cursor.execute('SELECT AVG(initial_risk_level) FROM Contacts WHERE client_pronouns LIKE "%She/Her%" and client_pronouns LIKE "%They/Them%"')
average = ((cursor.fetchall())[0])[0]
# assuming that by She/They we mean the contact uses both She/Her and They/Them pronouns as She/They as an exact match isn't an option
print("The average risk level of people who use 'She' and 'They' pronouns is", average)


connection.commit()
connection.close()