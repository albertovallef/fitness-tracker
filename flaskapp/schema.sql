CREATE TABLE IF NOT EXISTS user (
  u_userID INTEGER PRIMARY KEY AUTOINCREMENT,
  u_name TEXT UNIQUE NOT NULL,
  u_password TEXT NOT NULL,
  u_trainer BIT DEFAULT 0
);

CREATE TABLE IF NOT EXISTS  trainer (
  t_trainerID INTEGER PRIMARY KEY AUTOINCREMENT,
  t_userID INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS  customer (
  c_customerID INTEGER PRIMARY KEY AUTOINCREMENT,
  c_userID INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS subscription (
  su_subID INTEGER PRIMARY KEY AUTOINCREMENT,
  su_customerID INTEGER NOT NULL,
  su_trainerID INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS body (
  b_bodyID INTEGER PRIMARY KEY AUTOINCREMENT,
  b_userID INTEGER NOT NULL,
  b_age INTEGER NOT NULL,
  b_gender TEXT, 
  b_height INTEGER,
  b_weight INTEGER
);

CREATE TABLE IF NOT EXISTS exercise(
  e_exerciseID INTEGER PRIMARY KEY AUTOINCREMENT,
  e_name STRING NOT NULL
);
CREATE TABLE IF NOT EXISTS sets(
  s_setID INTEGER PRIMARY KEY AUTOINCREMENT,
  s_reps INTEGER, 
  s_weight INTEGER, 
  s_duration INTEGER
);
CREATE TABLE IF NOT EXISTS category(
  c_categoryID INTEGER PRIMARY KEY AUTOINCREMENT,
  c_name TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS  training_session(
  r_sessionID INTEGER PRIMARY KEY AUTOINCREMENT,
  r_userID INTEGER NOT NULL, 
  r_status BIT default 0, 
  r_datecompleted DATE 
);
CREATE TABLE IF NOT EXISTS workout(
  w_workoutID INTEGER PRIMARY KEY AUTOINCREMENT,
  w_sessionID INTEGER NOT NULL,
  w_exerciseID INTEGER NOT NULL,
  w_setID INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS ex_cat(
  ec_ID INTEGER PRIMARY KEY AUTOINCREMENT,
  ec_categoryID INTEGER NOT NULL,
  ec_exerciseID INTEGER NOT NULL
);