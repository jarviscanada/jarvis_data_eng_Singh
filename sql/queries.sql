
-- Q1: Show all members
SELECT * FROM cd.members;


-- ===== Modifying Data (pgexercises) =====

-- Q1: Insert some data into a table (updates/insert.html)
INSERT INTO cd.facilities
  (facid, name, membercost, guestcost, initialoutlay, monthlymaintenance)
VALUES
  (9, 'Spa', 20, 30, 100000, 800);

-- Q2: Insert calculated data into a table (updates/insert3.html)
INSERT INTO cd.facilities
  (facid, name, membercost, guestcost, initialoutlay, monthlymaintenance)
SELECT
  (SELECT MAX(facid) + 1 FROM cd.facilities),
  'Spa',
  20,
  30,
  100000,
  800;

-- Q3: Update some existing data (updates/update.html)
UPDATE cd.facilities
SET initialoutlay = 10000
WHERE facid = 1;

-- Q4: Update a row based on the contents of another row (updates/updatecalculated.html)
UPDATE cd.facilities f2
SET
  membercost = f1.membercost * 1.1,
  guestcost  = f1.guestcost  * 1.1
FROM cd.facilities f1
WHERE f1.facid = 0
  AND f2.facid = 1;

-- Q5: Delete all bookings (updates/delete.html)
DELETE FROM cd.bookings;

-- Q6: Delete a member with no bookings (updates/deletewh.html)
DELETE FROM cd.members
WHERE memid = 37
  AND memid NOT IN (
    SELECT memid
    FROM cd.bookings
  );

-- ===== Basics =====

-- Q7: Control which rows are retrieved - part 2 (basic/where2.html)
SELECT facid, name, membercost, monthlymaintenance
FROM cd.facilities
WHERE membercost > 0
  AND membercost < monthlymaintenance / 50
ORDER BY facid;

-- Q8: Basic string searches (basic/where3.html)
SELECT facid, name, membercost, guestcost, initialoutlay, monthlymaintenance
FROM cd.facilities
WHERE name LIKE '%Tennis%';

-- Q9: Matching against multiple possible values (basic/where4.html)
SELECT facid, name, membercost, guestcost, initialoutlay, monthlymaintenance
FROM cd.facilities
WHERE facid IN (1, 5)
ORDER BY facid;

-- Q10: Working with dates (basic/date.html)
SELECT memid, surname, firstname, joindate
FROM cd.members
WHERE joindate >= '2012-09-01'
ORDER BY joindate;

-- Q11: Combining results from multiple queries (basic/union.html)
SELECT surname
FROM cd.members
UNION
SELECT name AS surname
FROM cd.facilities
ORDER BY surname;

-- ===== Joins =====

-- Q12: Retrieve the start times of members' bookings (joins/simplejoin.html)
SELECT b.starttime
FROM cd.bookings b
JOIN cd.members m
  ON b.memid = m.memid
WHERE m.firstname = 'David'
  AND m.surname = 'Farrell'
ORDER BY b.starttime;

-- Q13: Work out the start times of bookings for tennis courts (joins/simplejoin2.html)
SELECT b.starttime AS start, f.name
FROM cd.bookings b
JOIN cd.facilities f
  ON b.facid = f.facid
WHERE f.name LIKE 'Tennis Court%'
  AND b.starttime >= '2012-09-21'
  AND b.starttime <  '2012-09-22'
ORDER BY b.starttime;

-- Q14: Produce a list of all members, along with their recommender (joins/self2.html)
SELECT
  m.firstname AS memfname,
  m.surname   AS memsname,
  r.firstname AS recfname,
  r.surname   AS recsname
FROM cd.members m
LEFT JOIN cd.members r
  ON m.recommendedby = r.memid
ORDER BY m.surname, m.firstname;

-- Q15: Produce a list of all members who have recommended another member (joins/self.html)
SELECT DISTINCT r.firstname, r.surname
FROM cd.members m
JOIN cd.members r
  ON m.recommendedby = r.memid
ORDER BY r.surname, r.firstname;

-- Q16: Produce a list of all members, along with their recommender, without using any joins (joins/sub.html)
SELECT DISTINCT
  m.firstname || ' ' || m.surname AS member,
  (
    SELECT r.firstname || ' ' || r.surname
    FROM cd.members r
    WHERE r.memid = m.recommendedby
  ) AS recommender
FROM cd.members m
ORDER BY member;

-- Q17: Count the number of recommendations each member makes (aggregates/count2.html)
SELECT
  recommendedby,
  COUNT(*) AS count
FROM cd.members
WHERE recommendedby IS NOT NULL
GROUP BY recommendedby
ORDER BY recommendedby;

-- Q18: List the total slots booked per facility (aggregates/fachours.html)
SELECT
  facid,
  SUM(slots) AS "Total Slots"
FROM cd.bookings
GROUP BY facid
ORDER BY facid;

-- Q19: List the total slots booked per facility in September 2012 (aggregates/fachours2.html)
SELECT
  facid,
  SUM(slots) AS "Total Slots"
FROM cd.bookings
WHERE starttime >= '2012-09-01'
  AND starttime <  '2012-10-01'
GROUP BY facid
ORDER BY "Total Slots";

-- Q20: List the total slots booked per facility per month in 2012 (aggregates/fachours3.html)
SELECT
  facid,
  EXTRACT(MONTH FROM starttime) AS month,
  SUM(slots) AS "Total Slots"
FROM cd.bookings
WHERE starttime >= '2012-01-01'
  AND starttime <  '2013-01-01'
GROUP BY facid, month
ORDER BY facid, month;

-- Q21: Find the count of members who have made at least one booking (including guests) (aggregates/members1.html)
SELECT
  COUNT(DISTINCT memid) AS count
FROM cd.bookings;

-- Q22: List each member with the date of their first booking after September 1st 2012 (aggregates/members2.html)
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

-- Q23: Produce a list of member names with the total number of members (aggregates/members3.html)
SELECT
  COUNT(*) OVER () AS count,
  firstname,
  surname
FROM cd.members
ORDER BY joindate;

-- Q24: Produce a monotonically increasing numbered list of members ordered by join date (aggregates/members4.html)
SELECT
  ROW_NUMBER() OVER (ORDER BY joindate) AS row_number,
  firstname,
  surname
FROM cd.members
ORDER BY joindate;

-- Q25: Output the facility id that has the highest number of slots booked (include ties) (aggregates/fachours4.html)
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

-- ===== String =====

-- Q26: Output the names of all members, formatted as 'Surname, Firstname' (string/concat.html)
SELECT
  surname || ', ' || firstname AS name
FROM cd.members
ORDER BY surname, firstname;

-- Q27: Find all telephone numbers that contain parentheses (string/reg.html)
SELECT
  memid,
  telephone
FROM cd.members
WHERE telephone ~ '[()]'
ORDER BY memid;

-- Q28: Count members by the first letter of their surname (string/substr.html)
SELECT
  SUBSTRING(surname, 1, 1) AS letter,
  COUNT(*) AS count
FROM cd.members
GROUP BY letter
ORDER BY letter;

