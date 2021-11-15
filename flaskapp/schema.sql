DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS trainer;
DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS subscription;
DROP TABLE IF EXISTS body;
DROP TABLE IF EXISTS exercise;
DROP TABLE IF EXISTS sets;
DROP TABLE IF EXISTS category;
DROP TABLE IF EXISTS routine;
DROP TABLE IF EXISTS ex_cat;

CREATE TABLE user (
  u_userId INTEGER PRIMARY KEY AUTOINCREMENT,
  u_name TEXT NOT NULL,
  u_password TEXT NOT NULL,
  u_trainer BIT DEFAULT 0
);

CREATE TABLE trainer (
  t_trainerId INTEGER PRIMARY KEY AUTOINCREMENT,
  t_userID INTEGER NOT NULL
);

CREATE TABLE customer (
  c_customerID INTEGER PRIMARY KEY AUTOINCREMENT,
  c_userID INTEGER NOT NULL
);

CREATE TABLE subscription (
  su_subID INTEGER PRIMARY KEY AUTOINCREMENT,
  su_customerID INTEGER NOT NULL,
  su_trainerID INTEGER NOT NULL
);

CREATE TABLE body (
  b_bodyID INTEGER PRIMARY KEY AUTOINCREMENT,
  b_userID INTEGER NOT NULL,
  b_age INTEGER NOT NULL,
  b_gender STRING, 
  b_height INTEGER,
  b_weight INTEGER
);

CREATE TABLE exercise(
  e_exerciseID INTEGER PRIMARY KEY AUTOINCREMENT,
  e_name STRING NOT NULL
);
CREATE TABLE sets(
  s_setID INTEGER PRIMARY KEY AUTOINCREMENT,
  s_reps INTEGER, 
  s_weight INTEGER, 
  s_duration INTEGER
);
CREATE TABLE category(
  c_categoryID INTEGER PRIMARY KEY AUTOINCREMENT,
  c_name STRING NOT NULL
);
CREATE TABLE routine(
  r_sessionID INTEGER PRIMARY KEY AUTOINCREMENT,
  r_userID INTEGER NOT NULL, 
  r_status BIT default 0, 
  r_datecreatedm DATE, 
  r_datecompleted DATE 
);
CREATE TABLE ex_cat(
  ec_ID INTEGER PRIMARY KEY AUTOINCREMENT,
  ec_categoryID INTEGER NOT NULL,
   ec_exerciseID INTEGER NOT NULL
);

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











INSERT into exercise (e_name) 
VALUES 
  ('bench press'),
  ('tricep push down'),
  ('incline bench press'),
  ('tricep overhead extension'),
  ('chest flies'),
  ('tricep dips'),
  ('chest hex press'),
  ('squat'),
  ('romanian deadlift'),
  ('leg press'),
  ('hip thrusts'),
  ('calf raises'),
  ('bulgarian split squat'),
  ('shoulder dumbell press'),
  ('shoulder side raises'),
  ('shoulder arnold press'),
  ('shoulder rear delt raises'),
  ('horizontal row'),
  ('barbell row'),
  ('upright row'),
  ('shoulder shrug'),
  ('deadlift'),
  ('pull ups'),
  ('lat pull down'),
  ('abdominal crunch'),
  ('leg raise'),
  ('oblique crunch'),
  ('bicep curl'),
  ('hammer curl'),
  ('preacher curl'),
  ('barbell curl'),
  ('cable pulldowns'),
  ('farmer walks'),
  ('pronated curls'),
  ('wrist curls'),
  ('chin up'),
  ('lunges');

INSERT into ex_cat (ec_categoryID, ec_exerciseID)
VALUES
  (5,1),
  (7,1),
  (5,2),
  (5,3),
  (7,3),
  (5,4),
  (7,5),
  (5,6),
  (7,7),
  (1,8),
  (2,8),
  (3,8),
  (4,8),
  (13,8),
  (13,9),
  (3,9),
  (9,10),
  (1,10),
  (2,10),
  (3,10),
  (13,10),
  (1,11),
  (3,11),
  (9,11),
  (13,11),
  (9,12),
  (1,12),
  (1,13),
  (2,13),
  (3,13),
  (9,13),
  (10,14),
  (10,15),
  (10,16),
  (10,17),
  (10,18),
  (10,19),
  (12,18),
  (12,19),
  (10,20),  
  (15,18),
  (15,19),
  (15,20),
  (11,20),
  (11,21),
  (14,22),
  (1,22),
  (3,22),
  (13,22),
  (12,23),
  (4,23),
  (15,23),
  (12,24),
  (15,24),
  (4,24),
  (8,25),
  (8,26),
  (2,26),
  (8,27),
  (4,28),
  (4,29),
  (4,30),
  (4,31),
  (5,32),
  (4,34),
  (6,33),
  (6,34),
  (6,35),
  (6,22),
  (6,23),
  (4,36),
  (15,36),
  (6,36),
  (1,37),
  (2,37),
  (3,37),
  (13,37),
  (9,37);