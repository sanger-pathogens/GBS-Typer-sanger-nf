import argparse
import io
import unittest
from unittest.mock import patch, call

from bin.get_targets_from_res_db import get_targets, write_line, write_fasta_file, write_target_fasta_files

class TestProcessResults(unittest.TestCase):

    TEST_TARGETS = 'test_data/seqs_of_interest.txt'
    TEST_FASTA = 'test_data/GBS_Res_Gene-DB_Final_0.0.1.fasta'

    def test_get_targets(self):
        actual = get_targets(self.TEST_TARGETS)
        self.assertEqual(actual, ['7__PARCGBS__PARCGBS-1__7',
            '5__GYRAGBS__GYRAGBS-1__5',
            '11__23S1__23S1-1__11',
            '12__23S3__23S3-3__12',
            '16__RPOBgbs__RPOBgbs-1__16',
            '17__RPOBgbs__RPOBgbs-2__17',
            '18__RPOBgbs__RPOBgbs-3__18',
            '19__RPOBgbs__RPOBgbs-4__19'])

    def setUp(self) -> None:
        self.test_stream = io.StringIO()

    def test_write_line(self):
        line = '>Target\n'
        actual = write_line(line, 'Target', 0, self.test_stream)
        self.assertEqual(actual, 1)

        line = 'ACTG'
        actual = write_line(line, 'Target', 1, self.test_stream)
        self.assertEqual(actual, 1)

        line = '>Seq'
        actual = write_line(line, 'Target', 0, self.test_stream)
        self.assertEqual(actual, 0)

    def test_write_fasta_file(self):
        write_fasta_file(self.TEST_FASTA, '7__PARCGBS__PARCGBS-1__7', 'test_data/CHECK_')
        f = open('test_data/CHECK_7__PARCGBS__PARCGBS-1__7_ref.fna', "r")
        actual = "".join(f.readlines())
        self.assertEqual(actual, """>7__PARCGBS__PARCGBS-1__7\nCATCCTCATGGGGATTCCTCTATTTATGACGCGATGGTTCGTATGTCTCAA\n""")

    @patch('bin.get_targets_from_res_db.write_fasta_file')
    def test_write_target_fasta_files(self, mock_write_fasta_file):
        targets = ['7__PARCGBS__PARCGBS-1__7',
            '5__GYRAGBS__GYRAGBS-1__5',
            '11__23S1__23S1-1__11',
            '12__23S3__23S3-3__12',
            '16__RPOBgbs__RPOBgbs-1__16',
            '17__RPOBgbs__RPOBgbs-2__17',
            '18__RPOBgbs__RPOBgbs-3__18',
            '19__RPOBgbs__RPOBgbs-4__19']
        write_target_fasta_files(targets, self.TEST_FASTA, 'test_data/CHECK_')
        mock_write_fasta_file.assert_has_calls([
            call(self.TEST_FASTA, '7__PARCGBS__PARCGBS-1__7', 'test_data/CHECK_'),
            call(self.TEST_FASTA, '5__GYRAGBS__GYRAGBS-1__5', 'test_data/CHECK_'),
            call(self.TEST_FASTA, '11__23S1__23S1-1__11', 'test_data/CHECK_'),
            call(self.TEST_FASTA, '12__23S3__23S3-3__12', 'test_data/CHECK_'),
            call(self.TEST_FASTA, '16__RPOBgbs__RPOBgbs-1__16', 'test_data/CHECK_'),
            call(self.TEST_FASTA, '17__RPOBgbs__RPOBgbs-2__17', 'test_data/CHECK_'),
            call(self.TEST_FASTA, '18__RPOBgbs__RPOBgbs-3__18', 'test_data/CHECK_'),
            call(self.TEST_FASTA, '19__RPOBgbs__RPOBgbs-4__19', 'test_data/CHECK_')
            ], any_order = False)
