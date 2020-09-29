PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE attachment(attachment_id INTEGER PRIMARY KEY, mail_id INTEGER, sender_id INTEGER NOT NULL, receiver_id INTEGER NOT NULL, attachment_file TEXT NOT NULL, FOREIGN KEY(mail_id) REFERENCES mail(mail_id));
INSERT INTO attachment VALUES(1,2,2,1,'web_test.xlsx');
INSERT INTO attachment VALUES(2,4,1,1,'dimension.xlsx');
CREATE TABLE user(user_id INTEGER PRIMARY KEY, user_name TEXT NOT NULL, user_email TEXT NOT NULL, user_password TEXT  NOT NULL, user_gender TEXT NOT NULL, user_date_of_birth TEXT NOT NULL, user_city TEXT NOT NULL, user_country TEXT NOT NULL, user_contact INTEGER, user_account_creation_date TEXT NOT NULL, user_active INTEGER DEFAULT 0 CHECK(user_active == 1 OR user_active == 0), UNIQUE(user_email));
INSERT INTO user VALUES(1,'Reda','reda@gmail.com','$2b$12$LjFCMwMFhMMU/pDrsD1BneT0JALhadvIm/ONu74Jow6sAD87hkxuK','Male','1970-02-02','Alexandria','Egypt',1066615431,'2020-09-21 06:40:25.995386',1);
INSERT INTO user VALUES(2,'Safaa','safaa@gmail.com','$2b$12$5wO320yp5i9J50Q.ZOgNdu0qTZCWN1VcH1rZPJFM1AwQTKXiCqftm','Female','1975-04-04','Alexandria','Egypt',1006615471,'2020-09-21 06:55:22.881296',1);
INSERT INTO user VALUES(3,'Medhat','medhat@gmail.com','$2b$12$o5fTzotncuVfqOJT94hnJ.iS7VrGUS8QNY8xYY8Yr4OKTfXl8QsAe','Male','1999-07-08','califorinia','America',1054784568,'2020-09-22 08:03:19.586705',0);
INSERT INTO user VALUES(4,'Mohamed','mohamed@gmail.com','$2b$12$3HOxvwpi6la8FrFkZbWbU.dxQRjH/GruACJJqsKqO5ycJCm.mDie.','Male','1999-11-11','Alexandria','Egypt',10283754,'2020-09-22 08:12:33.556651',1);
INSERT INTO user VALUES(5,'Ahmed','ahmed@gmail.com','$2b$12$qet99laeD5qwoiQVauZQuuqDOc3IEzwwT4BQB6wPRn9YBV2kxmARa','Male','2006-12-05','Alexandria','Egypt','019375t656','2020-09-22 08:33:04.246116',0);
INSERT INTO user VALUES(6,'Youssef','youssef@gmail.com','$2b$12$K2UTTx3HR/cSZl/3lERx9eRrad9E2eek40kz/0GrWxdhI.34MmT4e','Male','2006-08-08','Alexandria','Egypt',1839549674,'2020-09-22 08:44:21.568497',0);
CREATE TABLE mail(mail_id INTEGER PRIMARY KEY, sender_id INTEGER NOT NULL, receiver_id INTEGER NOT NULL, mail_subject TEXT, mail_body TEXT,  mail_date TEXT NOT NULL,mail_seen INTEGER DEFAULT 0 CHECK(mail_seen == 0 OR mail_seen == 1), sender_trashed INTEGER DEFAULT 0 CHECK(sender_trashed == 0 OR sender_trashed == 1), receiver_trashed INTEGER DEFAULT 0 CHECK(receiver_trashed == 0 OR receiver_trashed == 1), FOREIGN KEY(sender_id, receiver_id) REFERENCES user(user_id, user_id));
INSERT INTO mail VALUES(1,2,1,'VP meeting',replace(replace('Hey Reda I hope you are in a good form.\r\nI wanted to  remind you that there is a meeting tommorrow.','\r',char(13)),'\n',char(10)),'2020-09-21 06:57:20.756167',1,0,1);
INSERT INTO mail VALUES(2,2,1,'','see this file please.','2020-09-21 07:13:11.129603',1,0,0);
INSERT INTO mail VALUES(3,1,4,'Urgent Subject','I just wanted to inform you that you have a urgent meeting with the VP at 9:00 am tomorrow.','2020-09-22 18:12:25.882179',1,0,0);
INSERT INTO mail VALUES(4,1,1,'inbox color test','inbox color must change to red.','2020-09-22 18:19:34.391392',1,0,0);
INSERT INTO mail VALUES(5,1,3,'SUBJECT MEDHAT',replace(replace('1           Reda        reda@gmail.com  $2b$12$LjFCMwMFhMMU/pDrsD1BneT0JALhadvIm/ONu74Jow6sAD87hkxuK\r\n2           Safaa       safaa@gmail.co  $2b$12$5wO320yp5i9J50Q.ZOgNdu0qTZCWN1VcH1rZPJFM1AwQTKXiCqftm\r\n3           Medhat      medhat@gmail.c  $2b$12$o5fTzotncuVfqOJT94hnJ.iS7VrGUS8QNY8xYY8Yr4OKTfXl8QsAe\r\n4           Mohamed     mohamed@gmail.  $2b$12$3HOxvwpi6la8FrFkZbWbU.dxQRjH/GruACJJqsKqO5ycJCm.mDie.\r\n5           Ahmed       ahmed@gmail.co  $2b$12$qet99laeD5qwoiQVauZQuuqDOc3IEzwwT4BQB6wPRn9YBV2kxmARa\r\n6           Youssef     youssef@gmail.  $2b$12$K2UTTx3HR/cSZl/3lERx9eRrad9E2eek40kz/0GrWxdhI.34MmT4e\r\n8           Medhat      medhat@gmail.c  $2b$12$zZtENOd6FaTq9S4qFSXZD.J8G8sl2iDZtB.cesKbtz26VOtwcU35W','\r',char(13)),'\n',char(10)),'2020-09-22 18:26:37.716767',0,0,0);
DELETE FROM sqlite_sequence;
COMMIT;
