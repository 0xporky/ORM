#!/usr/bin/env python
#-*- coding: utf-8 -*-
import MySQLdb
import logging
from config import DATABASE_IP as ip
from config import DATABASE_USER as user
from config import DATABASE_USER_PASS as password
from config import DATABASE_NAME as db_name


class DbOrm(object):
    """
    Class implementing ORM for mysql data base
    """

    def __init__(self):
        logging.info('Starting logger for {0}'.format(db_name))
        self.logger = logging.getLogger(db_name)

    def connect(self):
        """
        Connecting to database using credentials.
        """
        try:
            self.db = MySQLdb.connect(ip, user, password, db_name)
        except Exception as e:
            self.logger.error(e)
            return False
        return True

    def close(self):
        """
        Free resourses and closes connection to database.
        """
        try:
            self.db.close()
        except Exception as e:
            self.logger.error(e)
            return False
        return True

    def select(self, table_name, columns, **kvargs):
        """
        Select procedure from table.
        Set where = {field: 'value', ... } to add WHERE condition.
        Set orderBy = {field1: 'ASC', field2: 'DESC'} to add ORDER BY condition.
        """
        self._check_params(table_name=table_name, columns=columns)

        cols = ', '.join(columns)
        sql = 'select {0} from {1}'.format(cols, table_name)

        where = kvargs.get('where')
        if where is not None and isinstance(where, dict):
            tmp = ' and '.join('{0}={1}'.format(key, value)
                               for key, value in where.items())
            sql = '{0} where {1}'.format(sql, tmp)

        orderBy = kvargs.get('orderBy')
        if orderBy is not None and isinstance(orderBy, dict):
            tmp = ', '.join('{0} {1}'.format(key, value)
                            for key, value in orderBy.items())
            sql = '{0} order by {1}'.format(sql, tmp)

        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as e:
            self.logger.error(e)
            return list()

    def update(self, table_name, params, condition):
        """
        Updating current table.
        """
        self._check_params(table_name=table_name,
                           params=params,
                           condition=condition)

        querySet = ', '.join('{0}={1}'.format(key, value)
                             for key, value in params.items())
        where = ' and '.join('{0}={1}'.format(key, value)
                             for key, value in condition.items())
        sql = 'update {0} set {1} where {2}'.format(table_name,
                                                    querySet,
                                                    where)
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            self.db.commit()
            return True
        except Exception as e:
            self.logger.error(e)
            self.db.rollback()
            return False

    def insert(self, table_name, params):
        """
        Inserting data to existing table.
        """
        self._check_params(table_name=table_name, params=params)

        keys = ", ".join("{}".format(key) for key in params)
        vals = ", ".join("'{}'".format(params[key]) for key in params)
        values = "({0}) values ({1})".format(keys, vals)

        sql = "insert into {0} {1}".format(table_name, values)

        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            self.db.commit()
            return cursor.lastrowid
        except Exception as e:
            self.logger.error(e)
            self.db.rollback()
            return -1

    def delete(self, table_name, params):
        """
        Deleting row from table.
        """
        self._check_params(table_name=table_name,
                           params=params)

        try:
            key = params.keys()[0]
            dict_params = "{0}={1}".format(key, params[key])
        except Exception as e:
            self.logger.error(e)

        sql = "delete from {0} where {1}".format(table_name, dict_params)

        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            self.db.commit()
            return True
        except Exception as e:
            self.logger.error(e)
            self.db.rollback()
            return False

    def _check_params(self, **kvargs):
        """
        Cheking inner function parameters.
        """
        table_name = kvargs.get('table_name')
        if table_name is not None:
            if not isinstance(table_name, str):
                raise Exception('Should set a database name.')
            if not len(table_name):
                raise Exception('Table name cannot be empty string.')

        params = kvargs.get('params')
        if params is not None:
            if not isinstance(params, dict):
                raise Exception('Should set params as dictionary.')
            if not len(params):
                raise Exception('Params canno be an empty dictionary.')

        condition = kvargs.get('condition')
        if condition is not None:
            if not isinstance(condition, dict):
                raise Exception('Should set condition as dictionary.')
            if not len(condition):
                raise Exception('Condition cannot be an empty dictionary.')

        columns = kvargs.get('columns')
        if columns is not None:
            if not isinstance(columns, list):
                raise Exception('Should set columns names')
            if not len(columns):
                raise Exception('List <colunms> cannot be empty.')
