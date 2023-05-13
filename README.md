Allie Version

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
4. From the format of this file, write down a database schema.
   * It's probably easiest if you turn in some equivalent to a bunch of create table statements in your return project
    * Diagrams available at [DBDiagram](https://dbdiagram.io/d/6453cdf9dca9fb07c483a5b7).

   create_table "contacts", force: :cascade do |t|
    t.integer "id" primary key
    t.datetime "time_call_began"
    t.datetime "time_call_ended"
    t.integer "initial_counselor_id"
    t.integer "total_transfers"
    t.string "issues_discussed"
    t.integer "call_rating"
    t.integer "initial_risk_level"
    t.string "client_pronouns"
    t.string "client_name"
    t.string "client_location"
  end

  create_table "counselors", force: :cascade do |t|
    t.integer "id" primary key
    t.string "name"
  end

  create_table "transfers", force: :cascade do |t|
    t.integer "id" primary key
    t.integer "contact_id"
    t.integer "counselor_id"
    t.datetime "timestamp"
  end
  
5. Now, write some code to clean this data, and insert it into your database. Here are some things to think about when writing your code:
   1. What concerns do you see?
      * Privacy concerns
      * COPPA concerns
      * PII concerns
      * Values are formatted differently, eg: \"Yu Yamada"\ vs. 'Yu Yamada'
      * Single transfer timestamps are formatted differently than mutli transfer timestamps
      * Timestamps don't have a timezone
      * If 2 counselors have the same name we have no way of knowing if they're 2 different people -> an improvement would be to assign each counselor a unique employee ID
   2. What choices have you made to clean the data?
      * Make timestamp format consistent
      * Remove extraneous symbols from strings (like [ and "')
      * Split data into 3 tables with joins to make data analysis cleaner
      * Added additional columns since the data is now split up (eg: initial_counselor_id and total_transfers)
   3. What choices have you made about the schema? Is this a relational database schema, or a big data one? (both choices are fine, just justify and explain yourself)
      * This is a relational database 
      * I wanted to use a relational database to take advantage of joins and reduce repetitive data
      * This will make my SQL queries more efficient
   4. If you were to scale your parsing code, what libraries/cloud technologies/strategies would you use to do so?
4. Now, write queries or code to answer the following questions again your populated database:
   1. Create an output csv with the data schema:
       * | COUNSELOR NAME  | DAY  | NUMBER OF CASES  | AVERAGE RISK LEVEL  | AVERAGE RATING  |
    2. The maximum number of concurrent cases handled by trevor at any time
    3. A list of counselors who dealt with more than one concurrent cases
    4. The average risk level of people who use `She/They` pronouns


# Submission
Once you are finished with the instructions above, please wrap this repository in a zip file and send it over to the recruiter 24 hours before your interview day and time. Ensure that your source code, instructions to run locally, and other documents you may have created. 

# Interview Information
A recruiter will be working with you to set up an interview day when you receive this project plan project. The interview will be 60 minutes with a Senior Data Engineer to go over your project plan, ask further past experience, and leave room for questions for you.

Breakdown of interview:
* 30 minutes: Project Plan Review
* 20 minutes: Past Experience Interview Questions
* 10 minutes: Q&A space for you
