--1 Inserts a new user (registration)
INSERT INTO user (u_name, u_password) VALUES (?, ?);

--2: Sets a user as a trainer by putting their u_userID into the trainer table (registration)
INSERT INTO trainer (t_userID)
    SELECT u_userID FROM user
    WHERE u_name = ? AND
          u_password = ?;

--3 Selects a user from the user table with the given u_name and u_password (login)
SELECT * FROM user 
WHERE u_name = ? AND
      u_password = ?;

--4: Sets a user as a customer by putting their u_userID into the customer table
INSERT INTO customer (c_userID)
    SELECT u_userID FROM user
    WHERE u_name = ? AND
          u_password = ?;

--5: Search exercise by category
SELECT e_name
  FROM category,
       exercise,
       ex_cat
 WHERE ec_categoryID = c_categoryID AND
       ec_exerciseID = e_exerciseID AND
       c_name = ?;

--6: Search by exercise name
SELECT e_name
  FROM exercise
 WHERE e_name = ?;


--7: Populating category table:
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

--8 selects all exercises from exercise table so user 
--  can select an exercise from the list of exercises
SELECT e_name
  FROM exercise
 ORDER BY e_name;


-----------------------QUERIES FOR ADDING A WORKOUT----------------------
--9 First we create a new training session which contains all workouts performed during that session
INSERT INTO training_session (r_userID, r_datecompleted) VALUES (?, ?);

--10 Then we create the set based on USERs s_reps, s_weight, and s_duration
INSERT INTO sets (s_reps, s_weight, s_duration) VALUES (?, ?, ?);

--11 Add a workout
INSERT into workout (w_sessionID, w_excerciseID, w_setID)
SELECT r_sessionID, e_exerciseID, s_setID
from 
(SELECT r_sessionID from training_session where r_userID = ? and r_datecompleted = ?), 
(select e_exerciseID from exercise where e_name = ?), 
(select s_setID from sets where s_reps = ? and s_weight = ? and s_duration = ?)


--12 Select the name, exercise, sets, reps, and weight
SELECT e_name,
       s_setID,
       s_reps,
       s_weight
  FROM user,
       training_session,
       workout,
       sets,
       exercise
 WHERE u_userID = r_userID AND
       w_setID = s_setID AND
       w_exerciseID = e_exerciseID and
       u_name = ?;


--13 Calculate progress by selecting average weight between date range for a
-- specific user and exercise
SELECT AVG(s_weight)
  FROM user,
       training_session,
       workout,
       sets,
       exercise
 WHERE u_userID = r_userID AND
       w_setID = s_setID AND
       w_exerciseID = e_exerciseID AND
       u_name = ? AND
       e_name = ? AND
       r_datecompleted BETWEEN ? AND ?;

--14 Returns all exercises done on a specific date
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
       r_datecompleted = ? AND
       u_name = ?
 GROUP BY s_setID
 ORDER BY e_name;


--15 Search for workouts by exercise
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
--16 Add new subscription
INSERT INTO subscription (su_customerID, su_trainerID) VALUES (?, ?);

--17 Select the user id from customer table
SELECT c_customerID
FROM user, customer
WHERE u_userID = c_userID AND
      u_name = ?;

-----------------BODY---------------------
--18 Insert body foir each created user
INSERT INTO body (b_age, b_gender, b_height, b_weight)
    SELECT u_userID, ?,?,? FROM user
    WHERE u_name = ?
    AND u_password = ?;


--19 Edit Body
UPDATE body
   SET b_height = ?
  FROM user
 WHERE b_userID = u_userID AND
       u_name = ?;


--20 Show Body
SELECT b_age,
       b_gender,
       b_height,
       b_weight
  FROM body,
       user
 WHERE u_userID = b_userID AND
       u_name = ?;

--20 Show number of repetitions of all exercises
SELECT SUM(s_reps)
  FROM user,
       training_session,
       workout,
       sets,
       exercise
 WHERE u_userID = r_userID AND
       w_setID = s_setID AND
       w_exerciseID = e_exerciseID AND
       u_name = ? AND
       e_name = ? AND
       r_datecompleted BETWEEN ? AND ?;

