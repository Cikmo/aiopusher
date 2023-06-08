# Contributing

Prior to contributing to this repository, please reach out to the owner of this repository to discuss the changes you wish to make either through creating an issue, emailing the owner, or any other preferred method of communication. 


## Installation
pusher-client uses [Poetry](https://python-poetry.org/) to manage the dependencies. After getting poetry, install the dependencies, run the following command:
```sh
poetry install
```
> **Note:** If your changes require additional modules, please add them using `poetry add <module-name> --group <appropriate group>`, or by adding them to the `pyproject.toml` file manually in the appropriate group. If done manually make sure to run `poetry lock` to update the `poetry.lock` file.


## Formatting
As the source code formatter, rwar uses [black](https://pypi.org/project/black/). Ensure you run the following command after your changes have been implemented.
```sh
black ./pusher_client ./tests/
```
> **Note:** If you are using VSCode, you can set the following settings to automatically format your code on save:
> ```json
> "editor.formatOnSave": true
> "python.formatting.provider": "black"
> ```

## Linting

pusher-client follows the [PEP8](https://www.python.org/dev/peps/pep-0008/) style guide and uses [pylint](https://pypi.org/project/pylint/) to enforce this. To lint your code, run the following command:
```sh
pylint ./pusher_client ./tests/
```
> **Note:** If you are using VSCode, you can install the [pylint extension](https://marketplace.visualstudio.com/items?itemName=ms-python.pylint) to dynamically analyze your code and display errors and warnings in the editor.

## Testing 

pusher-client uses [pytest](https://docs.pytest.org/en/stable/) to run tests. To run the tests, run the following command:
```sh
pytest
```

You can also run the tests on multiple python versions using [nox](https://nox.thea.codes/en/stable/). To run the tests on all supported python versions, run the following command:
```sh
nox -s test
```