--1 (inserts a new user)
INSERT INTO user (u_name, u_password) VALUES (?, ?)

--2 Selects a user from the user table with the given u_name and u_password (for login)
SELECT * FROM user 
WHERE u_name = ? 
AND u_password = ?;

--3: Sets a user as a trainer by putting their u_userID into the trainer table
INSERT INTO trainer (t_userID)
    Select u_userID from user 
    where u_name = ? 
    and u_password = ?;

--4: Sets a user as a customer by putting their u_userID into the customer table
INSERT INTO customer (c_userID)
    Select u_userID from user 
    where u_name = ? 
    and u_password = ?;

--5: Search by category
SELECT e_name from category, exercise, ex_cat
    where ec_categoryID = c_categoryID
    and ec_exerciseID = e_exerciseID
    and c_name = ?;

--6: Search by workout name
SELECT e_name from exercise
    where e_name = ?;

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
SELECT e_name FROM exercise 
    Order by e_name;


-----------------------QUERIES FOR ADDING A WORKOUT----------------------
--9 Add a workout (This might end up being multiple queuries
--Need to get the exercise, sets, reps, and weight from user and add it in


-- Returns all exercises done on a specific date
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


-- Search for workouts by exercise
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

