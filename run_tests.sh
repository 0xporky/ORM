#!/bin/bash
PYTHONPATH=$1 python ./tests/test_orm.py
PYTHONPATH=$1 python ./tests/test_user.py
