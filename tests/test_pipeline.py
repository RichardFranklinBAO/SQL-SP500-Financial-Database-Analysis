"""Reproducible end-to-end checks without downloading external datasets."""
import math
import sqlite3
import tempfile
import unittest
from pathlib import Path
from src.build_database import ROOT, build

class DatabaseTests(unittest.TestCase):
    def test_demo_and_rebuild_guard(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / 'demo.sqlite'
            build(ROOT / 'data/demo', target)
            with sqlite3.connect(target) as db:
                counts = {name:db.execute(f'SELECT COUNT(*) FROM {name}').fetchone()[0]
                          for name in ['companies','macro_indicators','stock_prices','sp500_returns','sector_summary']}
                self.assertEqual(counts, {'companies':3, 'macro_indicators':3,
                                          'stock_prices':9,'sp500_returns':9,'sector_summary':6})
                r = db.execute('SELECT avg_return,ticker_count FROM sector_summary WHERE summary_date=? AND sector=?',
                               ('2017-01-03','Technology')).fetchone()
                self.assertEqual(r[1],2)
                self.assertTrue(math.isclose(r[0],(0.01+0.04)/2,abs_tol=1e-12))
                self.assertEqual(db.execute('PRAGMA integrity_check').fetchone()[0],'ok')
            with self.assertRaises(FileExistsError):
                build(ROOT/'data/demo',target)
            build(ROOT/'data/demo',target,overwrite=True)

if __name__ == '__main__':
    unittest.main()
