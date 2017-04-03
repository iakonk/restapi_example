CREATE TABLE IF NOT EXISTS 'registered_members' (
    'id' INTEGER PRIMARY KEY  AUTOINCREMENT,
    'f_name' varchar(50) DEFAULT NULL,
    'l_name' varchar(50) DEFAULT NULL,
    'primary_skill' varchar(200) DEFAULT NULL,
    'email' varchar(50) DEFAULT NULL,
    'phone' varchar(25) DEFAULT NULL
);
