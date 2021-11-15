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