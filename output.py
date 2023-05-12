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
    # since im doing it between original cases and transfers I can't use the AVG method
    # instead I need to SUM and divide the risk levels
    cursor.execute('SELECT SUM(initial_risk_level), SUM(call_rating) FROM Contacts WHERE initial_counselor_id=?', (counselor_id,))
    contacts_data = ((cursor.fetchall())[0])
    sum_case_risk_levels = contacts_data[0]
    sum_case_ratings = contacts_data[1]
    cursor.execute('SELECT contact_id FROM Transfers WHERE counselor_id=?', (counselor_id,))
    transfer_contact_ids = (cursor.fetchall())
    sum_transfer_risk_levels = 0
    sum_transfer_rating_levels = 0
    for contact_id in transfer_contact_ids:
        cursor.execute('SELECT initial_risk_level, call_rating FROM Contacts WHERE id=?', (contact_id[0],))
        transfers_data = ((cursor.fetchall())[0])
        sum_transfer_risk_levels = sum_transfer_risk_levels + transfers_data[0]
        sum_transfer_rating_levels = sum_transfer_rating_levels + transfers_data[1]
    total_sum_risk_level = sum_case_risk_levels + sum_transfer_risk_levels
    average_risk_level = total_sum_risk_level / total_cases_with_transfers
    # DRAWBACK if a chat is transferred BACK to a counselor that already had it then it will consider that contact more than once in the average
    output_data.append(average_risk_level)
    total_sum_ratings = sum_case_ratings + sum_transfer_rating_levels
    average_ratings = total_sum_ratings / total_cases_with_transfers
    output_data.append(average_ratings)
    cursor.execute('insert into Output(COUNSELOR_NAME, DAY, NUMBER_OF_CASES, AVERAGE_RISK_LEVEL, AVERAGE_RATING) values (?,?,?,?,?)', output_data,)
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