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

```sh
# I had to install the project again to update the command entrypoints.
# i.e. use `poetry install` if the bin installed by poetry (in the virtual env) is out of date.
poetry install
poetry shell
```

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

Unfortunately, the requirements specifically state to use the testing package that comes with Python (and not `pytest`) i.e. won't be able to use `capsys`.

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

I went with using `subprocess.run` but I did have a look at the suggested solution first and they're using a more "white box" testing approach where they assert the result of `argparse` (and so tie the tests to that library). On the plus side, these tests don't depend on any installed script so they could run outside `poetry`.

```py
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

```

Running

```
python -m unittest

----------------------------------------------------------------------
Ran 0 tests in 0.000s

OK
```

i.e. nothing runs and not 100% sure why (maybe the file structure I'm using?).

but running:

```
poetry run python -m unittest
..
----------------------------------------------------------------------
Ran 2 tests in 0.100s

OK
```

… works. NOTE: would need to run `python3 -m unittest` in my case and `klickbrick` script needs to be installed locally (see next section) for tests to work as that's how they're designed (tests run script).

## Building and installing locally

From [https://dev.to/mattioo/publish-a-package-on-pypi-using-poetry-5e5](https://dev.to/mattioo/publish-a-package-on-pypi-using-poetry-5e5), looks like you can build the package with `poetry build`.

Then install it in your local "env" (not virtual env) using `pip`, in my case, I had to use the `pip` of a specific Python version (so that it matches with the `python` I used to develop the package - as opposed to the `python` associated with the `pip` on my `$PATH`):

`python3 -m pip install dist/klickbrick-0.1.0-py3-none-any.whl`

where `dist/klickbrick-0.1.0-py3-none-any.whl` was generated from `build` earlier.

You can now run `klickbrick`.

To uninstall:

`python3 -m pip uninstall klickbrick`

## Publishing to pypi test

First create an account here: https://test.pypi.org/

From [poetry publish docs](https://python-poetry.org/docs/cli/#publish), running `poetry publish -r <repositoryName>`:

> --repository (-r): The repository to register the package to (default: pypi). Should match a repository name set by the config command.

i.e. if we're to deploy to the test `pypi` repository (or "registry" as I seem to know it from `npm` ("repo" is associated with "git repo" to my mind)), then it's necessary to first run `poetry config` to include the location of the new registry in the `toml` file.

I am going to copy this from the solution; yes I've exceeded the time I've allowed myself on this and am now looking at the solution. As long as I understand what's going on, I don't mind. So, in `.travis.yml`, there's this section:

```yml
before_deploy:
  - poetry build
  - poetry config repositories.testpypi https://test.pypi.org/legacy/
  - poetry config http-basic.testpypi $TEST_PYPI_USERNAME $TEST_PYPI_PASSWORD
```

It looks like the solution leaves it until the pipeline process is running to register the test registry. Fair enough, but I'll do it locally too.

So, looks like I was wrong and running: `poetry config repositories.testpypi https://test.pypi.org/legacy/`, does not change the `toml` file, however, running `poetry config --list` displays the new config setting: `repositories.testpypi.url = "https://test.pypi.org/legacy/"`

The travis config file uses:

```yml
script: poetry publish -r testpypi
```

so `testpypi` should be enough as an argument when `poetry publish`ing to pick the value of `repositories.testpypi.url` from the config.

But of course, if I try to publish, I get an error - why would anything be simple? Just like on any registry, if the name is taken, then you're not going to be able to publish over it of course. That's why namespaces are such a good idea. No idea if they're supported in `pypi`, so just going with a different name.

After some digging around looks like I need to make the following adjustments to my `toml` file:

```toml
[tool.poetry]
name = "justinc-klickbrick"
packages = [
  {include = "klickbrick", from = "src"},
]
```

i.e. I renamed the package to `justinc-klickbrick` - that didn't look taken from a quick search on test pypi. Then, I had to add the `packages` section. I think this is because I'm using the `src` directory to structure the project.

Anyway, that's all the changes necessary AFAICT.

```
rm -rf ./dist
poetry build
python3 -m pip install ./dist/justinc_klickbrick-0.1.0-py3-none-any.whl
# can now run klickbrick at cli
python3 -m pip uninstall justinc-klickbrick
```

This works now: `poetry publish -r testpypi`. btw, if you don't store creds (or token) in config, then you get asked for creds when publishing. Also, looks like test pypi registry gets cleaned (from what I read), so users and packages might simply be deleted over time i.e. the following link might not host the package anymore:

https://test.pypi.org/project/justinc-klickbrick/

Great. Now, if I run: `poetry run python -m unittest`, the tests are broken with:

```
FileNotFoundError: [Errno 2] No such file or directory: 'klickbrick'
```

So looks like `klickbrick` got uninstalled and the tests fail as they are dependent on having an installed `klickbrick` script. Maybe this is because of `rm -rf ./dist` from before the package renaming. Anyway, to fix this I had to: `poetry install` again. I guess that puts the listed (in toml file) scripts in poetry env as well as installs dependencies.

Anyway, still don't meet the following requirement:

> The unit test should be executable from the command line by running python -m unittest so it can be easily run in TravisCI.

First of all, because I depend on `klickbrick` being installed... I guess I'd have to always use `poetry run` for this.

I have confirmed the following works:

```sh
python3 -m pip install ./dist/justinc_klickbrick-0.1.0-py3-none-any.whl
python3 -m unittest
# stdout:
..
----------------------------------------------------------------------
Ran 2 tests in 0.115s

OK
```

i.e. after installing this package, I have `klickbrick` script available for tests to pass.

So, if you're not going to change testing approach, then CI is going to have to install this package before running tests.

To confirm, but looking at the travis file, looks like this "installation before testing" is already happening there.

## CI part

https://docs.travis-ci.com/user/build-stages/

> Build stages is a way to group jobs, and run jobs in each stage in parallel, but run one stage after another sequentially.

Not going to spend too much time researching this. I get the idea; I don't know all the config options. Just going to copy the solution's config more or less. Using the exact version of `python` I happen to have installed as the default one on my PATH i.e. `3.7.4`, and not using `make`… can one assume `make` is always installed? Does it make sense to use it? Right now, not really as there's no dependencies between tasks (i.e. solution Makefile is just aliasing commands).

Also, not using integration tests (not sure why they're called integration tests - they're still white box tests i.e. tests at the `argsparse` level). The tests in this repo are already integration tests for this project as they run the script directly.

i.e. no BDD tests using `behave`.

TODO: need to figure out the nuances of travis config e.g.

- use of `script: skip` - I would assume simply doesn't run a script for the job.
- looks like there's a lifecycle of sorts (`... script, before_deploy, deploy ...`).
- what's `deploy.skip_cleanup`? What does `cleanup` involve?
- what's the extent of what you can do in `if:`?
- I imagine I need to tag the commit myself and it won't pick up a version bump in `toml` file and do the tagging automatically?

## Test after CI deploy to test pypi

After confirming that `klickbrick` script is uninstalled on my system:

```
python3 -m pip install --index-url https://test.pypi.org/simple/ justinc-klickbrick
# now running klickbrick works
# and this uninstalls it:
python3 -m pip uninstall justinc-klickbrick
```

To commit to this repo and not trigger the CI build use `[ci skip]` in commit message (probably needs to be at end of first line), e.g.

```
git commit -m 'test update [ci skip]'
```
