# Introduction

This folder contains my PostgreSQL SQL practice for the RDBMS & SQL module. The goal of this work is to build strong fundamentals by solving a structured set of real-world style exercises using the `cd.members`, `cd.facilities`, and `cd.bookings` tables. The solutions cover CRUD operations, filtering, joins (including self-joins and subqueries), aggregation with `GROUP BY`/`HAVING`, window functions (such as `ROW_NUMBER()` and `COUNT() OVER()`), and common string operations.

Each question is documented in this README with a formatted SQL snippet, while the complete set of solutions is also stored in `queries.sql` for quick execution and review. This makes it easy for a reviewer to verify correctness, understand the approach, and assess SQL competency in a consistent, readable format.


###### Table Setup (DDL)

The `cd.members`, `cd.facilities`, and `cd.bookings` tables were created by loading the official pgExercises sample dataset (`clubdata.sql`) into PostgreSQL.

```bash
cd ~/dev/jarvis_data_eng_Singh/sql
export PGPASSWORD='password'
psql -h localhost -U postgres -d postgres -f clubdata.sql
```

###### Question 1: Show all members

```sql
SELECT * FROM cd.members;

```
###### Modifying Data - Insert some data into a table (insert.html)

```sql
INSERT INTO cd.facilities
  (facid, name, membercost, guestcost, initialoutlay, monthlymaintenance)
VALUES
  (9, 'Spa', 20, 30, 100000, 800);
```

###### Modifying Data - Insert calculated data into a table (insert3.html)

```sql
INSERT INTO cd.facilities
  (facid, name, membercost, guestcost, initialoutlay, monthlymaintenance)
SELECT
  (SELECT MAX(facid) + 1 FROM cd.facilities),
  'Spa',
  20,
  30,
  100000,
  800;
```

###### Modifying Data - Update some existing data (update.html)

```sql
UPDATE cd.facilities
SET initialoutlay = 10000
WHERE facid = 1;
```

###### Modifying Data - Update a row based on the contents of another row (updatecalculated.html)

```sql
UPDATE cd.facilities f2
SET
  membercost = f1.membercost * 1.1,
  guestcost  = f1.guestcost  * 1.1
FROM cd.facilities f1
WHERE f1.facid = 0
  AND f2.facid = 1;
```

###### Modifying Data - Delete a member with no bookings (deletewh.html)

```sql
DELETE FROM cd.members
WHERE memid = 37
  AND memid NOT IN (
    SELECT memid
    FROM cd.bookings
  );
```

###### Basics - Control which rows are retrieved - part 2 (where2.html)

```sql
SELECT facid, name, membercost, monthlymaintenance
FROM cd.facilities
WHERE membercost > 0
  AND membercost < monthlymaintenance / 50
ORDER BY facid;
```

### Basics - Basic string searches (where3.html)

```sql
SELECT facid, name, membercost, guestcost, initialoutlay, monthlymaintenance
FROM cd.facilities
WHERE name LIKE '%Tennis%';
```

### Basics - Matching against multiple possible values (where4.html)

```sql
SELECT facid, name, membercost, guestcost, initialoutlay, monthlymaintenance
FROM cd.facilities
WHERE facid IN (1, 5)
ORDER BY facid;
```

### Basics - Working with dates (date.html)

```sql
SELECT memid, surname, firstname, joindate
FROM cd.members
WHERE joindate >= '2012-09-01'
ORDER BY joindate;
```

### Basics - Combining results from multiple queries (union.html)

```sql
SELECT surname
FROM cd.members
UNION
SELECT name AS surname
FROM cd.facilities
ORDER BY surname;
```

###### Joins - Retrieve the start times of members' bookings (simplejoin.html)

```sql
SELECT b.starttime
FROM cd.bookings b
JOIN cd.members m
  ON b.memid = m.memid
WHERE m.firstname = 'David'
  AND m.surname = 'Farrell'
ORDER BY b.starttime;
```

###### Joins - Work out the start times of bookings for tennis courts (simplejoin2.html)
```sql
SELECT b.starttime AS start, f.name
FROM cd.bookings b
JOIN cd.facilities f
  ON b.facid = f.facid
WHERE f.name LIKE 'Tennis Court%'
  AND b.starttime >= '2012-09-21'
  AND b.starttime <  '2012-09-22'
ORDER BY b.starttime;
```

####### Joins - Produce a list of all members, along with their recommender (self2.html)

```sql
SELECT
  m.firstname AS memfname,
  m.surname   AS memsname,
  r.firstname AS recfname,
  r.surname   AS recsname
FROM cd.members m
LEFT JOIN cd.members r
  ON m.recommendedby = r.memid
ORDER BY m.surname, m.firstname;
```

##### Joins - Produce a list of all members who have recommended another member (self.html)

```sql
SELECT DISTINCT r.firstname, r.surname
FROM cd.members m
JOIN cd.members r
  ON m.recommendedby = r.memid
ORDER BY r.surname, r.firstname;
```

#### Joins - Produce a list of all members, along with their recommender, without using any joins (sub.html)

```sql
SELECT DISTINCT
  m.firstname || ' ' || m.surname AS member,
  (
    SELECT r.firstname || ' ' || r.surname
    FROM cd.members r
    WHERE r.memid = m.recommendedby
  ) AS recommender
FROM cd.members m
ORDER BY member;
```

##### Aggregates - Count the number of recommendations each member makes (count2.html)

```sql
SELECT
  recommendedby,
  COUNT(*) AS count
FROM cd.members
WHERE recommendedby IS NOT NULL
GROUP BY recommendedby
ORDER BY recommendedby;
```

###### Aggregates - List the total slots booked per facility (fachours.html)
```sql
SELECT
  facid,
  SUM(slots) AS "Total Slots"
FROM cd.bookings
GROUP BY facid
ORDER BY facid;
```

#### Aggregates - List the total slots booked per facility in September 2012 (fachours2.html)
```sql
SELECT
  facid,
  SUM(slots) AS "Total Slots"
FROM cd.bookings
WHERE starttime >= '2012-09-01'
  AND starttime <  '2012-10-01'
GROUP BY facid
ORDER BY "Total Slots";
```

###### Aggregates - List the total slots booked per facility per month in 2012 (fachours3.html)
```sql
SELECT
  facid,
  EXTRACT(MONTH FROM starttime) AS month,
  SUM(slots) AS "Total Slots"
FROM cd.bookings
WHERE starttime >= '2012-01-01'
  AND starttime <  '2013-01-01'
GROUP BY facid, month
ORDER BY facid, month;
```

#### Aggregates - Find the count of members who have made at least one booking (including guests) (members1.html)
```sql
SELECT
  COUNT(DISTINCT memid) AS count
FROM cd.bookings;
```

#### Aggregates - List each member with the date of their first booking after September 1st 2012 (members2.html)
```sql
SELECT
  m.surname,
  m.firstname,
  b.memid,
  MIN(b.starttime) AS starttime
FROM cd.bookings b
JOIN cd.members m
  ON m.memid = b.memid
WHERE b.starttime >= '2012-09-01'
GROUP BY m.surname, m.firstname, b.memid
ORDER BY b.memid;
```

#### Aggregates - Produce a list of member names with the total number of members (members3.html)
```sql
SELECT
  COUNT(*) OVER () AS count,
  firstname,
  surname
FROM cd.members
ORDER BY joindate;
```

#### Aggregates - Produce a monotonically increasing numbered list of members ordered by join date (members4.html)
```sql
SELECT
  ROW_NUMBER() OVER (ORDER BY joindate) AS row_number,
  firstname,
  surname
FROM cd.members
ORDER BY joindate;
```

#### Aggregates - Output the facility id that has the highest number of slots booked (include ties) (fachours4.html)
```sql
SELECT
  facid,
  SUM(slots) AS total
FROM cd.bookings
GROUP BY facid
HAVING SUM(slots) = (
  SELECT MAX(total_slots)
  FROM (
    SELECT SUM(slots) AS total_slots
    FROM cd.bookings
    GROUP BY facid
  ) x
);
```

#### String - Output the names of all members, formatted as 'Surname, Firstname' (concat.html)

```sql
SELECT
  surname || ', ' || firstname AS name
FROM cd.members
ORDER BY surname, firstname;
```

#### String - Find all telephone numbers that contain parentheses (reg.html)
```sql
SELECT
  memid,
  telephone
FROM cd.members
WHERE telephone ~ '[()]'
ORDER BY memid;
```

#### String - Count members by the first letter of their surname (substr.html)
```sql
SELECT
  SUBSTRING(surname, 1, 1) AS letter,
  COUNT(*) AS count
FROM cd.members
GROUP BY letter
ORDER BY letter;
```

