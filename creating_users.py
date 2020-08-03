from admin import admin
from user import user
import os

allUsers = []
adminOfApplication = admin('omar','omarredaelsayedmohamed@gmail.com','admin123','male','6/6/2000','Alexandria','Egypt','01065630331')

user1 = user('youssef','mailerfirstmailerlast@gmail.com','FirstLast11','Male','8/8/2006','Alexandria','Egypt','01265630331')
user1.set_appPassword(os.environ.get('FirstMailerPassword'))

user2 = user('Ahmed','mailersecondmailerlast@gmail.com','SecondLast11','Male','5/12/2006','Alexandria','Egypt','01006615471')
user2.set_appPassword(os.environ.get('SecondMailerPassword'))

user3 = user('Omar','omarredaelsayedmohamed@gmail.com','Shahen77','Male','6/6/2000','Alexandria','Egypt','01065630331')
user3.set_appPassword(os.environ.get('mailPassword'))

allUsers.append(user1)
allUsers.append(user2)
allUsers.append(user3)