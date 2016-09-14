#!/usr/bin/env python
#-*- coding: utf-8 -*-

import unittest
import MySQLdb

from config import DATABASE_IP as ip
from config import DATABASE_USER as user
from config import DATABASE_USER_PASS as password
from config import DATABASE_NAME as db_name

from models.user import User


class UserTest(unittest.TestCase):

    def setUp(self):

        self.table_name = 'users'

        db = MySQLdb.connect(ip, user, password)
        cursor = db.cursor()

        cursor.execute('DROP DATABASE IF EXISTS {0}'.format(db_name))
        db.commit()

        cursor.execute('CREATE DATABASE {0}'.format(db_name))
        db.commit()
        db.close()
        db = MySQLdb.connect(ip, user, password, db_name)

        cursor = db.cursor()
        cursor.execute("""CREATE TABLE {0}(
                         id INT NOT NULL AUTO_INCREMENT,
                         fullName varchar(150),
                         email varchar(150),
                         password varchar(30),
                         avatar varchar(255),
                         isActive boolean,
                         role_id INT,
                         PRIMARY KEY (id))""".format(self.table_name))
        db.commit()

        cursor.execute("""INSERT INTO {0}
                       (fullName,
                       email,
                       password,
                       avatar,
                       isActive,
                       role_id)
                       VALUES(
                            "test0",
                            "test@gmail.com",
                            "12345",
                            "avatar.jpg",
                            TRUE,
                            1)""".format(self.table_name))
        db.commit()

        db.close()

        self.user = User()

    def tearDown(self):
        self.user.close()

        db = MySQLdb.connect(ip, user, password)
        cursor = db.cursor()

        cursor.execute('DROP DATABASE IF EXISTS {0}'.format(db_name))
        db.commit()
        db.close()

    def test_user_create(self):
        """Creating user in database."""
        result = self.user.create_user(fullName='test1',
                                       email='test1@email.com',
                                       password='12345',
                                       avatar='avatar.jpg',
                                       isActive=1,
                                       role_id=2)
        self.assertNotEquals(result, -1)

    def test_user_delete(self):
        """Deleting user from database."""
        result = self.user.delete_user(1)
        self.assertTrue(result)

    def test_update_user(self):
        """Updating user data."""
        result = self.user.update_user_data(user_id=2, fullName='"test3"')
        self.assertTrue(result)

    def test_select_users(self):
        """Selecting one user by ID."""
        result = self.user.select_users()
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
