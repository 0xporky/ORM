#!/usr/bin/env python
#-*- coding: utf-8 -*-

import unittest
import MySQLdb
from models.dborm import DbOrm

from config import DATABASE_IP as ip
from config import DATABASE_USER as user
from config import DATABASE_USER_PASS as password
from config import DATABASE_NAME as db_name


class OrmTest(unittest.TestCase):

    def setUp(self):

        self.table_name = 'test'

        db = MySQLdb.connect(ip, user, password)
        cursor = db.cursor()

        cursor.execute('CREATE DATABASE {0}'.format(db_name))
        db.commit()
        db.close()
        db = MySQLdb.connect(ip, user, password, db_name)

        cursor = db.cursor()
        cursor.execute("""CREATE TABLE {0}(
                         id INT NOT NULL AUTO_INCREMENT,
                         name varchar(150),
                         age INT,
                         PRIMARY KEY (id))""".format(self.table_name))
        db.commit()

        cursor.execute("""INSERT INTO {0}
                       (name, age)
                       VALUES("test0", 19)""".format(self.table_name))
        db.commit()

        cursor.execute("""INSERT INTO {0}
                       (name, age)
                       VALUES("test1", 20)""".format(self.table_name))
        db.commit()

        db.close()

        self.orm = DbOrm()
        self.orm.connect()

    def tearDown(self):
        self.orm.close()

        db = MySQLdb.connect(ip, user, password)
        cursor = db.cursor()

        cursor.execute('DROP DATABASE IF EXISTS {0}'.format(db_name))
        db.commit()
        db.close()

    def test_insert(self):
        """Check insert command."""
        result = self.orm.insert(self.table_name, {'name': 'test3', 'age': 20})
        self.assertNotEqual(result, -1)

        result2 = self.orm.insert(self.table_name, {'name': 'test4'})
        self.assertNotEqual(result2, -1)

    def test_select(self):
        """Selecting query without conditions."""
        result = self.orm.select(self.table_name,
                                 ['id', 'name', 'age'])
        self.assertNotEqual(len(result), 0)

        result2 = self.orm.select(self.table_name, ['name'])
        self.assertNotEqual(len(result2), 0)

    def test_select_where(self):
        """Select query with WHERE condition."""
        result = self.orm.select(self.table_name,
                                 ['name', 'age'],
                                 where={'age': 19})
        self.assertNotEqual(len(result), 0)

    def test_select_order(self):
        """Select query with ORDER BY condition."""
        result = self.orm.select(self.table_name,
                                 ['id', 'name', 'age'],
                                 orderBy={'age': 'ASC'})
        self.assertNotEqual(len(result), 0)

    def test_update(self):
        """Update query test."""
        result = self.orm.update(self.table_name,
                                 {'age': 25},
                                 {'id': 1})
        self.assertTrue(result)

    def test_delete(self):
        """Delete query test."""
        result = self.orm.delete(self.table_name,
                                 {'id': 2})
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
