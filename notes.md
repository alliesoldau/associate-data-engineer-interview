# Instructions
1. Clone this repository to your local computer.
2. Review the README for instructions.
3. Looking at the `client_records.jsonl` file, what questions do you have about the meaning of the data?
4. From the format of this file, write down a database schema.
   * It's probably easiest if you turn in some equivalent to a bunch of create table statements in your return project
   ** [DBDiagram](https://dbdiagram.io/d/6453cdf9dca9fb07c483a5b7)
5. Now, write some code to clean this data, and insert it into your database. Here are some things to think about when writing your code:
   1. What concerns do you see?
   2. What choices have you made to clean the data?
   3. What choices have you made about the schema? Is this a relational database schema, or a big data one? (both choices are fine, just justify and explain yourself)
   4. If you were to scale your parsing code, what libraries/cloud technologies/strategies would you use to do so?
4. Now, write queries or code to answer the following questions again your populated database:
   1. Create an output csv with the data schema:
       * | COUNSELOR NAME  | DAY  | NUMBER OF CASES  | AVERAGE RISK LEVEL  | AVERAGE RATING  |
    2. The maximum number of concurrent cases handled by trevor at any time
    3. A list of counselors who dealt with more than one concurrent cases
    4. The average risk level of people who use `She/They` pronouns

