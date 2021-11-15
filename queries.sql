--1
SELECT * FROM user 
WHERE u_name = ? 
AND u_password = ?;

--2
INSERT INTO user (u_name, u_password) VALUES (?, ?)

--3: Sets a user as a trainer by putting their u_userID into the trainer table
INSERT INTO trainer (t_userID)
    Select u_userID from user 
    where u_name = ? 
    and u_password = ?;