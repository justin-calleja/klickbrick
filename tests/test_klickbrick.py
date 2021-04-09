import os
import unittest

# from klickbrick.cli import hello_cmd

# import subprocess

# def test_greet_cli2():
#     result = subprocess.run(["greet", "America/Costa_Rica"], capture_output=True)
#     assert b"Costa Rica!" in result.stdout


class TestStringMethods(unittest.TestCase):
    def test_x(self):
        """
        Can this package be run as a Python module?
        """
        exit_status = os.system('python -m klickbrick --help')
        assert exit_status == 0

    # def test_upper(self):
    #     result = hello_cmd(["hello"])
    #     # result = subprocess.run(
    #     # ["klickbrick", "hello"], capture_output=True)
    #     self.assertEqual(result, "Hello World")

    # self.assertEqual('foo'.upper(), 'FOO')

    # def test_isupper(self):
    #     self.assertTrue('FOO'.isupper())
    #     self.assertFalse('Foo'.isupper())

    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)


if __name__ == '__main__':
    unittest.main()
