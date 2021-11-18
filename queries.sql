--1 Inserts a new user (registration)
INSERT INTO user (u_name, u_password) VALUES (?, ?);

--2: Sets a user as a trainer by putting their u_userID into the trainer table (registration)
INSERT INTO trainer (t_userID)
    SELECT u_userID FROM user
    WHERE u_name = ? AND
          u_password = ?;

--3: Update trainer bit in user (adding trainers)
UPDATE user
Set u_trainer = 1
where u_name = ?
and u_password = ?

--4 Selects a user from the user table with the given u_name and u_password (login)
SELECT * FROM user 
WHERE u_name = ? AND
      u_password = ?;

--5: Sets a user as a customer by putting their u_userID into the customer table
INSERT INTO customer (c_userID)
    SELECT u_userID FROM user
    WHERE u_name = ? AND
          u_password = ?;

--6: Search exercise by category
SELECT e_name
  FROM category,
       exercise,
       ex_cat
 WHERE ec_categoryID = c_categoryID AND
       ec_exerciseID = e_exerciseID AND
       c_name = ?;

--7: Search exercise ID by exercise name
SELECT e_exerciseID
  FROM exercise
 WHERE e_name = ?;


--8: Populating category table:
INSERT into category (c_name)
    VALUES
    ('legs'),
    ('quad'),
    ('hamstring'),
    ('bicep'),
    ('tricep'),
    ('forearm'),
    ('chest'),
    ('core'),
    ('calves'),
    ('delts'),
    ('traps'),
    ('lats'),
    ('glutes'),
    ('lower back'),
    ('upper back');

--9 Select all exercises names from exercise table in alphabetical order
-- (user needs to see all possible exercises to select from when adding workout)
SELECT e_name
  FROM exercise
 ORDER BY e_name;


-----------------------QUERIES FOR ADDING A WORKOUT----------------------
--10 First we create a new training session which contains all workouts performed during that session
INSERT INTO training_session (r_userID, r_datecompleted)
SELECT u_userID, ? FROM user
    WHERE u_name = ?;

--11 Then we create the set based on USERs s_reps, s_weight, and s_duration
INSERT INTO sets (s_reps, s_weight, s_duration) VALUES (?, ?, ?);

--12 Add a workout
INSERT into workout (w_sessionID, w_exerciseID, w_setID)
SELECT r_sessionID, e_exerciseID, ?
from
(SELECT r_sessionID from training_session, user where r_userID = u_userID AND u_name = ? and r_datecompleted = ?),
(select e_exerciseID from exercise where e_name = ?);


--13 Show all workouts completed by a user
SELECT e_name,
       s_setID,
       s_reps,
       s_weight,
       r_datecompleted
  FROM user,
       training_session,
       workout,
       sets,
       exercise
 WHERE u_userID = r_userID AND
       w_setID = s_setID AND
       w_sessionID = r_sessionID AND
       w_exerciseID = e_exerciseID AND
       u_name = ?;


--14 Calculate progress by selecting average weight between date range for a *****************************
-- specific user and exercise
SELECT AVG(s_weight),
       r_datecompleted
  FROM user,
       training_session,
       workout,
       sets,
       exercise
 WHERE u_userID = r_userID AND
       w_setID = s_setID AND
       w_sessionID = r_sessionID AND
       w_exerciseID = e_exerciseID AND
       u_name = ? AND
       e_name = ? AND
       r_datecompleted BETWEEN ? AND ?
       group by r_datecompleted;

--15 Returns all exercises done on a specific date
SELECT r_datecompleted,
       e_name,
       s_reps,
       s_weight
  FROM training_session,
       exercise,
       sets,
       workout,
       user
 WHERE w_sessionID = r_sessionID AND
       w_exerciseID = e_exerciseID AND
       w_setID = s_setID AND
       u_userID = r_userID AND
       u_name = ? AND
       r_datecompleted = ?
 GROUP BY s_setID
 ORDER BY e_name, s_weight ASC;

--16 Search for workouts details by exercise name
SELECT r_datecompleted,
       e_name,
       s_reps,
       s_weight
  FROM training_session,
       exercise,
       sets,
       workout,
       user
 WHERE w_sessionID = r_sessionID AND
       w_exerciseID = e_exerciseID AND
       u_userID = r_userID AND
       w_setID = s_setID AND
       e_name = ? AND
       u_name = ?
 GROUP BY s_setID
 ORDER BY r_datecompleted;

----------------SUBSCRIPTIONS---------------
--17 Add new subscription (trainer name taken from UI and customer from flask session)
INSERT INTO subscription (su_trainerID, su_customerID)
select t_trainerID, c_customerID from
(Select t_trainerID from user, trainer where t_userID = u_userID and u_name = ?),
(select c_customerID from user, customer where u_userID = c_userID and u_name = ?);


--18 Select all workouts from a trainer the user is subscribed to on a given date.**********************************
SELECT r_datecompleted,
       e_name,
       s_reps,
       s_weight
FROM user u1,
user u2,
customer,
trainer,
subscription,
training_session,
workout,
exercise,
sets
where
u1.u_userID = c_userID AND
c_customerID = su_customerID AND
t_trainerID = su_trainerID AND
u2.u_name = ? AND --trainer name
u1.u_name = ? AND --user name
r_userID = u2.u_userID AND
w_exerciseID = e_exerciseID AND
r_sessionID = w_sessionID AND
s_setID = w_setID AND
r_datecompleted = ?;


-----------------BODY---------------------
--19 Insert body for each created user
INSERT INTO body (b_userID, b_age, b_gender, b_height, b_weight)
Select u_userID, ?,?,?,? from
(SELECT u_userID from user
    where u_name = ?
    and u_password = ?)


--20 Edit Body (would be same for height, weight, age)
UPDATE body
   SET b_weight = ?
  FROM user
 WHERE b_userID = u_userID AND
       u_name = ?;


--21 Show Body
SELECT b_age,
       b_gender,
       b_height,
       b_weight
  FROM body,
       user
 WHERE u_userID = b_userID AND
       u_name = ?;


--22 Unsubscribe customer from trainer
DELETE FROM subscription
      WHERE su_trainerID IN (
                SELECT t_trainerID
                  FROM user,
                       trainer
                 WHERE u_userID = t_userID
                 and u_name = ?
            )
AND
            su_customerID IN (
    SELECT c_customerID
      FROM user,
           customer
     WHERE u_userID = c_userID
     and u_name = ?
);