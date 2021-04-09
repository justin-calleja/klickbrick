Starting point: I have very little exp with Python but am not new to programming.

These are my notes / log while trying to complete: [build-an-extensible-cli-with-python](https://www.manning.com/liveproject/build-an-extensible-cli-with-python)

## Read the argparse tutorial

[argparse tutorial](https://docs.python.org/3/howto/argparse.html#concepts)

## Install and get minimially familiar with poetry

[poetry](https://python-poetry.org/docs/)

I understand the virtual env concept but am not comfortable with the commands to switch and examine the envs.

## Read [python-module-vs-package](https://dev.to/bowmanjd/python-module-vs-package-4m8e)

Great read. Links to the following. TODO: read:

- https://towardsdatascience.com/whats-init-for-me-d70a312da583

## Read [getting-started-with-python-poetry](https://dev.to/bowmanjd/getting-started-with-python-poetry-3ica)

### Initialize the project with poetry

Creates an `src` dir with a package in it. Seems like a good idea:

```sh
poetry new --name klickbrick --src klickbric
```

### Using the virtual environment

Looks like you can drop in a Python REPL with the correct virtual env for the project using `poetry run python`:

> The poetry run command will execute the command in the virtual environment. For instance, try the following:

```sh
[pygreet]$ poetry run python
```

> Executing a shell in the virtual environment (i.e. activating it) is also possible with poetry shell after which we can execute python or other commands.

There's also a section on this in `poetry`'s [Basic usage](https://python-poetry.org/docs/basic-usage/) (goes into how to exit and other alternatives like getting the virtual env without starting a sub shell).

Create test and run it with `poetry run pytest`

## Follow up blog post [build-command-line-tools-with-python-poetry](https://dev.to/bowmanjd/build-command-line-tools-with-python-poetry-4mnc)

Demos how to add a mapping of script name to Python function in `poetry`'s `pyproject.toml`. Then goes into how to `install` that script in the virtual env and dropping into it to use it.

Good tip on testing - use `sys.argv[1:]` as input to your cli args parser so you can actually test it. Similar to `process.argv.slice(2)` in Node.js.

```py
def cli(args=None):
    """Process command line arguments."""
    if not args:
        args = sys.argv[1:]
    tz = args[0]
    print(greet(tz))
```

Use of [pytest's capsys](https://docs.pytest.org/en/stable/reference.html?highlight=capsys#std-fixture-capsys) to capture `stdout` and make assertions on it:

```py
    captured = capsys.readouterr()
    result = captured.out
    assert "San Juan!" in result
```

> Note that we could write a test using subprocess.run(), and that appears to work as well.

```py
import subprocess

def test_greet_cli2():
    result = subprocess.run(["greet", "America/Costa_Rica"], capture_output=True)
    assert b"Costa Rica!" in result.stdout
```

This seems to be pretty useful since we're required to use `unittest` not `pytest` (i.e. won't have access to `capsys`).

> Note that we could write a test using subprocess.run(), and that appears to work as well.

```py
import subprocess

def test_greet_cli2():
    result = subprocess.run(["greet", "America/Costa_Rica"], capture_output=True)
    assert b"Costa Rica!" in result.stdout
```

Links to other cli creation tools:

- https://palletsprojects.com/p/click/
- https://github.com/google/python-fire

TODO: read https://dev.to/bowmanjd/build-a-command-line-interface-with-python-poetry-and-click-1f5k
TODO: read https://dev.to/bowmanjd/python-tools-for-managing-virtual-environments-3bko

## Add unittest test

https://docs.python.org/3/library/unittest.html
