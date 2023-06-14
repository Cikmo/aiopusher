# Contributing

Prior to contributing to this repository, please reach out to the owner of this repository to discuss the changes you wish to make either through creating an issue, emailing the owner, or any other preferred method of communication.

---

## Installation

aiopusher uses [Poetry](https://python-poetry.org/) to manage the dependencies. After getting poetry, install the dependencies, run the following command:

```sh
poetry install
```

> **Note:** If your changes require additional modules, please add them using `poetry add <module-name> --group <appropriate group>`, or by adding them to the `pyproject.toml` file manually in the appropriate group. If done manually make sure to run `poetry lock` to update the `poetry.lock` file.

## Testing and Linting

### Testing

aiopusher uses [pytest](https://docs.pytest.org/en/stable/) to run tests. To run the tests, run the following command:

```sh
pytest
```

You can also run the tests on multiple python versions. Make sure you have the appropriate python versions installed, I recommend using [pyenv](https://github.com/pyenv/pyenv) for this. To run the tests on all supported python versions, run the following command:

```sh
nox -s test
```

### Formatting

As the source code formatter, aiopusher uses [black](https://pypi.org/project/black/). You can check if your code is formatted correctly by running the following command:

```sh
nox -s black
```

> **Note:** If you are using VSCode, I recommend installing the [black extension](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter) to automatically format your code in editor. You can also set it to automatically format your code on save.

### Linting

pusher-client follows the [PEP8](https://www.python.org/dev/peps/pep-0008/) style guide and uses [pylint](https://pypi.org/project/pylint/) to enforce this. To lint your code, run the following command:

```sh
nox -s lint
```

> **Note:** If you are using VSCode, you can install the [pylint extension](https://marketplace.visualstudio.com/items?itemName=ms-python.pylint) to dynamically analyze your code and display errors and warnings in the editor.

## Type Checking

pusher-client uses [pyright](https://microsoft.github.io/pyright/#/) to perform static type checking. To run the type checker, run the following command with the virtual environment activated:

```sh
nox -s typecheck
```

> **note:** I recommend installing the [pylance extension](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) (which is powered by pyright) with strict mode enabled to dynamically analyze your code and display errors and warnings in the editor.

### You can also run all of the tests and checks above commands at once by running the following command

```sh
nox
```

---

## Documentation
