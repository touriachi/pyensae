"""
@brief      test log(time=1s)

You should indicate a time in seconds. The program ``run_unittests.py``
will sort all test files by increasing time and run them.
"""


import sys
import os
import unittest


try:
    import src
    import pyquickhelper as skip_
except ImportError:
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..")))
    if path not in sys.path:
        sys.path.append(path)
    path = os.path.normpath(
        os.path.abspath(
            os.path.join(
                os.path.split(__file__)[0],
                "..",
                "..",
                "..",
                "pyquickhelper",
                "src")))
    if path not in sys.path:
        sys.path.append(path)
    import src
    import pyquickhelper as skip_

from pyquickhelper.loghelper import fLOG
from src.pyensae.sql.database_helper import import_flatfile_into_database
from src.pyensae.sql.database_main import Database


class TestDatabaseInsert (unittest.TestCase):

    def test_import_index(self):
        fLOG(
            __file__,
            self._testMethodName,
            OutputPrint=__name__ == "__main__")
        file = os.path.join(
            os.path.abspath(
                os.path.split(__file__)[0]),
            "data",
            "ACA.PA.txt")
        dbf = os.path.join(
            os.path.abspath(
                os.path.split(__file__)[0]),
            "temp_database_index.db3")
        if os.path.exists(dbf):
            os.remove(dbf)
        import_flatfile_into_database(dbf, file, fLOG=fLOG)
        assert os.path.exists(dbf)
        db = Database(dbf, LOG=fLOG)
        db.connect()

        db.create_index("index1", "ACAPA", "Date")
        li = db.get_index_list()
        self.assertEqual(
            li, [('index1', 'ACAPA', 'CREATE INDEX index1 ON ACAPA (Date)', ('Date',))])
        line = db.get_table_nfirst_lines("ACAPA")
        col = [_[0] for _ in db.get_table_columns("ACAPA")]
        line = line[0]
        add = {k: v for k, v in zip(col, line)}
        db.insert("ACAPA", add)
        db.commit()
        db.update("ACAPA", "Date", add["Date"], add)
        db.commit()

        db.close()

if __name__ == "__main__":
    unittest.main()
