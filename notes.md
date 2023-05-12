# Instructions
1. Clone this repository to your local computer.
2. Review the README for instructions.
3. Looking at the `client_records.jsonl` file, what questions do you have about the meaning of the data?
4. From the format of this file, write down a database schema.
   * It's probably easiest if you turn in some equivalent to a bunch of create table statements in your return project
    * Diagrams available at [DBDiagram](https://dbdiagram.io/d/6453cdf9dca9fb07c483a5b7).

   create_table "contacts", force: :cascade do |t|
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
    t.string "name"
  end

  create_table "transfers", force: :cascade do |t|
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
   2. What choices have you made to clean the data?
      * Make timestamp format consistent
      * Remove extraneous symbols from strings (like [ and "')
      * Split data into 3 tables with joins to make data analysis cleaner
      * Added additional columns since the data is now split up (eg: initial_counselor_id and total_transfers)
   3. What choices have you made about the schema? Is this a relational database schema, or a big data one? (both choices are fine, just justify and explain yourself)
   4. If you were to scale your parsing code, what libraries/cloud technologies/strategies would you use to do so?
4. Now, write queries or code to answer the following questions again your populated database:
   1. Create an output csv with the data schema:
       * | COUNSELOR NAME  | DAY  | NUMBER OF CASES  | AVERAGE RISK LEVEL  | AVERAGE RATING  |
    2. The maximum number of concurrent cases handled by trevor at any time
    3. A list of counselors who dealt with more than one concurrent cases
    4. The average risk level of people who use `She/They` pronouns

