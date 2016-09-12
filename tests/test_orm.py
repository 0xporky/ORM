import unittest
from models.dborm import DbOrm


class OrmTest(unittest.TestCase):

    def setUp(self):
        self.db = DbOrm()
        self.db.connect()

    def tearDown(self):
        self.db.close()

    def test_select(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
