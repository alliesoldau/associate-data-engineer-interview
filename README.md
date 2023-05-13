_Allie's answers are in italics_

# Associate Data Engineer Project Plan Interview
> This repository contains the project plan instructions for the Associate Data Engineer role.
Feel free to contact the recruiter for any follow-up questions in regards to the instructions and submissions.

# Context
> This take-home project plan should take a maximum of 4 hours to complete, which means, it's possible to complete in less than the recommended max time. 

You will be provided with a file in this repository called `client_records.jsonl`, which contains 100,000 (fake) client records in JSONL format with sensible keys. For the purpose of this assignment, please provide the source code you create inside this repository along with instructions for our team to run the code. 

Any common language and database is OK for this purpose. If you make some unorthodox decision (i.e., "I'm spinning up a cassandra cluster for these 100,000 rows, and I'm parsing the JSONL using Lisp!"), with your design, it would probably be a wise decision to justify why the choices you're making are the best ones for this use case.

# Instructions
1. Clone this repository to your local computer.
2. Review the README for instructions.
3. Looking at the `client_records.jsonl` file, what questions do you have about the meaning of the data?
   * _Are we assuming all counselor names are unique, or are duplicates possible?_
   * _Do all timestamps have the same timezone? What is the timezone?_
   * _If a chat transfers away from a counselor, and then BACK to the original counselor is that considered one chat or 2 for that counselor?_
   * _Are we concerned with keeping track of each youth who reaches out or are we ignoring that for this case sense we normally monitor that with IP addresses?_
   * _Why are all of these chats on the same day? A counselor having 7k+ chats at once seems off. Is this intentional? Or just a byproduct of using Faker?_
   * _Is there a heirarchy of the order for issues discussed? Is the first issue mentioned the primary issue?_
   * _I am assuming no duplicate contacts are recorded in the file. Is this accurate? If we are assuming duplicates I would have added in a check for duplicity in the data cleaning._

4. From the format of this file, write down a database schema.
   * It's probably easiest if you turn in some equivalent to a bunch of create table statements in your return project
    * _Visual diagrams available at [DBDiagram](https://dbdiagram.io/d/6453cdf9dca9fb07c483a5b7)._

   _cursor.execute('Create Table if not exists Counselors (id integer primary key, name string)')_

   _cursor.execute('Create Table if not exists Contacts (id integer primary key, time_call_began datetime, time_call_ended datetime, call_rating integer, initial_risk_level integer, client_name string, client_location string, client_pronouns string, issues_discussed string, initial_counselor_id integer, total_transfers integer)')_

   _cursor.execute('Create Table if not exists Transfers (id integer primary key, contact_id integer, counselor_id integer, timestamp datetime)')_
  
5. Now, write some code to clean this data, and insert it into your database. Here are some things to think about when writing your code:
      * _I wrote the ETL in python so that it could be adapted easily to a service for automating this process._
      * _I opted to omit passwords and encrypting the information to simplify the solution. In a real-world-scenario this would be important._
   1. What concerns do you see?
      * _Privacy concerns_
      * _COPPA concerns_
      * _PII concerns_
      * _String values are formatted differently, eg: \"Yu Yamada"\ vs. 'Yu Yamada'_
      * _Single transfer timestamps are formatted differently than mutli transfer timestamps_
      * _Timestamps don't have a timezone_
      * _If 2 counselors have the same name we have no way of knowing if they're 2 different people -> an improvement would be to assign each counselor a unique employee ID_
   2. What choices have you made to clean the data?
      * _Make timestamp format consistent_
      * _Remove extraneous characters from strings (like [ and "')_
      * _Split data into 3 tables (Contacts, Counselors, and Transfers) with joins to make data analysis cleaner_
         * _Each transfer gets it's own row in the Transfer table which makes it easier to access the data_
      * _Added additional columns since the data is now split up (eg: initial_counselor_id and total_transfers)_
   3. What choices have you made about the schema? Is this a relational database schema, or a big data one? (both choices are fine, just justify and explain yourself)
      * _This is a relational database_ 
      * _I wanted to use a relational database to take advantage of joins and reduce repetitive data_
      * _This will make my SQL queries more efficient_
   4. If you were to scale your parsing code, what libraries/cloud technologies/strategies would you use to do so?
      * _Apache Airflow: an open-source workflow management platform. I think the python would translate into this with relative ease_
      * _Snowflake: an elastically scalable cloud data warehouse. I think it would take some more effort to translate over to snowflake but their built in Snowsql database management would be nice since it keeps everything in one platform. Also it's good for running multiple queries at once which would be beneficial for Trevor since understanding our contacts' needs is so important and because we may need to run queries to support buisness decisions like headcount and financial needs._ 
4. Now, write queries or code to answer the following questions again your populated database:
   * _Question 1 populate as a seperate CSV file and questions 2-4 will print to the terminal when the files are run. I also pasted the answers for 2-4 below for easy reference._
   1. Create an output csv with the data schema:
       * | COUNSELOR NAME  | DAY  | NUMBER OF CASES  | AVERAGE RISK LEVEL  | AVERAGE RATING  |
    2. The maximum number of concurrent cases handled by trevor at any time
      * _The maximum number of concurrent cases handled by trevor at any time is 94982 cases_
    3. A list of counselors who dealt with more than one concurrent cases
      * _The list contains all of the counselors in the database_
      * _The counselors who dealt with more than one concurrent cases are as follows: [['Yu Yamada'], ['Carlos Khan'], ['Yan Delacroix'], ['Marsha Tanaka'], ['Fumiko Stevens'], ['Hans Wang'], ['Hui Ivanovich'], ['Mary Farouk'], ['Mary Kim'], ['Lou Roberts'], ['Frank LópezPatel'], ['Persephone Sun'], ['Hans Yamada'], ['Claude Roberts'], ['Ibrahim Li'], ['Beth Chen'], ['Claude Kant'], ['Sri Farouk'], ['Maria Tanaka'], ['Ibrahim Tanaka'], ['Fatima Stryker'], ['Zoë Ivanovich'], ['Kumar Ali'], ['Susan Smith'], ['Olga Ramanujan']]_
    4. The average risk level of people who use `She/They` pronouns
      * _The average risk level of people who use 'She' and 'They' pronouns is 3.010087116001834_


# Submission
Once you are finished with the instructions above, please wrap this repository in a zip file and send it over to the recruiter 24 hours before your interview day and time. Ensure that your source code, instructions to run locally, and other documents you may have created. 

# Interview Information
A recruiter will be working with you to set up an interview day when you receive this project plan project. The interview will be 60 minutes with a Senior Data Engineer to go over your project plan, ask further past experience, and leave room for questions for you.

Breakdown of interview:
* 30 minutes: Project Plan Review
* 20 minutes: Past Experience Interview Questions
* 10 minutes: Q&A space for you
