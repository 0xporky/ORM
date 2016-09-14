#!/usr/bin/env python
#-*- coding: utf-8 -*-

from models.user import User
import MySQLdb
from config import DATABASE_IP as ip
from config import DATABASE_USER as db_user
from config import DATABASE_USER_PASS as password
from config import DATABASE_NAME as db_name


if __name__ == '__main__':
        db = MySQLdb.connect(ip, db_user, password)
        cursor = db.cursor()

        cursor.execute('DROP DATABASE IF EXISTS {0}'.format(db_name))
        db.commit()

        cursor.execute('CREATE DATABASE {0}'.format(db_name))
        db.commit()
        db.close()
        db = MySQLdb.connect(ip, db_user, password, db_name)

        cursor = db.cursor()
        cursor.execute("""CREATE TABLE {0}(
                         id INT NOT NULL AUTO_INCREMENT,
                         fullName varchar(150),
                         email varchar(150),
                         password varchar(30),
                         avatar varchar(255),
                         isActive boolean,
                         role_id INT,
                         PRIMARY KEY (id))""".format('users'))
        db.commit()

        db.close()

        user = User()
        print('Creating new user.')
        result = user.create_user(fullName='test1',
                                  email='test1@email.com',
                                  password='12345',
                                  avatar='avatar.jpg',
                                  isActive=1,
                                  role_id=2)
        print('Result... {0}'.format(result))

        print('Creating new user.')
        result = user.create_user(fullName='test2',
                                  email='test2@email.com',
                                  password='12345',
                                  avatar='avatar.jpg',
                                  isActive=1,
                                  role_id=3)
        print('Result... {0}'.format(result))

        user.select_users()

        for u in user:
            print(u)

        print('Deleting user.')
        user.delete_user(1)
        print('Done.')

        user.select_users()
        for u in user:
            print(u)

        print('Updating user name.')
        user.update_user_data(2, fullName='"andrew"')
        user.select_user(2)
        print(user)

        user.close()

        db = MySQLdb.connect(ip, db_user, password)
        cursor = db.cursor()

        cursor.execute('DROP DATABASE IF EXISTS {0}'.format(db_name))
        db.commit()
        db.close()
