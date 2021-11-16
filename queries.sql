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
Select e_name, s_reps, s_weight
from training_session, exercise, sets, workout
where w_sessionID = r_sessionID
and w_exerciseID = e_exerciseID
and r_datecompleted = ?
order by e_name
group by s_setID;


-- Search for workouts by exercise
Select r_datecompleted, s_reps, s_weight
from training_session, exercise, sets, workout
where w_sessionID = r_sessionID
and w_exerciseID = e_exerciseID
and e_name = ?
order by r_datecompleted
group by s_setID;
