import unittest
import subprocess


class TestKlickbrickCli(unittest.TestCase):
    def test_hello_arg(self):
        """
        "hello" arg prints "Hello World"
        """
        result = subprocess.run(
            ["klickbrick", "hello"], capture_output=True)
        assert b"Hello World" in result.stdout

    def test_hello_arg_with_name(self):
        """
        "hello" arg with "--name Ole" prints "Hello Ole"
        """
        result = subprocess.run(
            ["klickbrick", "hello", "--name", "Ole"], capture_output=True)
        assert b"Hello Ole" in result.stdout


if __name__ == '__main__':
    unittest.main()
