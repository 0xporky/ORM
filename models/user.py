#!/usr/bin/env python
#-*- coding: utf-8 -*-

from dborm import DbOrm


class User(object):

    def __init__(self):
        self._table_name = 'users'
        self._initfields()
        self._orm = DbOrm()
        self._orm.connect()

    def close(self):
        """Free resourses and closing connections to database."""
        self._orm.close()

    def create_user(self, **kvargs):
        """Creating new user in database."""
        args_l = kvargs.keys()
        self_l = self.fields
        unset_args = [a for a in self_l if a not in args_l and a is not 'id']

        print(unset_args)

        if len(unset_args) > 0:
            arg_str = ', '.split(unset_args)
            msg = 'Not enought arguments. Needed {0}'.format(arg_str)
            raise Exception(msg)

        if 'id' in kvargs.keys():
            raise Exception('Cannot insert <id> value into database.')

        result = self._orm.insert(self._table_name, kvargs)

        if result is True:
            for key, value in kvargs:
                if kvargs.get(key) is not None and key in self.__dict__:
                    self.__dict__[key] = value

        return result

    def delete_user(self, user_id):
        """Deleting user by id."""
        return self._orm.delete(self._table_name, {'id': user_id})

    def update_user_data(self, user_id, **kvargs):
        """Updating some user fields."""
        args_l = kvargs.keys()
        self_l = self.fields
        diff_args = [a for a in args_l if a not in self_l]

        if len(diff_args) > 0:
            fields = ', '.join(diff_args)
            msg = 'Unreachable user fields {0}.'.format(fields)
            raise Exception(msg)

        return self._orm.update(self._table_name, kvargs, {'id': user_id})

    def select_user(self, user_id):
        """Selecting one user by ID."""
        fields = self.fields
        result = self._orm.select(self._table_name,
                                  fields,
                                  where={'id': user_id})

        if len(result) == 0:
            return False

        for field in self.fields:
            self.__dict__[field] = result[0][self.fields.index(field)]

        return True

    def select_users(self):
        """Selecting all users from the table."""
        fields = self.fields
        result = self._orm.select(self._table_name, fields)

        if len(result) == 0:
            return False

        for field in self.fields:
            self.__dict__[field] = result[0][self.fields.index(field)]

        return True

    def __repr__(self):
        return 'id:{0} user:{1}'.format(self.id, self.fullName)

    def _initfields(self):
        """Init service fields for model."""
        self.fields = ['id',
                       'fullName',
                       'email',
                       'password',
                       'avatar',
                       'isActive',
                       'role_id']
        for field in self.fields:
            self.__dict__[field] = None
