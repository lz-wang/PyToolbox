# PyToolbox for lzwang

This is a personal Python library for lzwang' daily usage.

## Tools List

- Logger: [loguru](src/logger.py), [pylogger](src/pylogger.py)
- File tools: [file tools](src/file.py)
- Achieve tools: [7zip tools](src/7zip.py)
- Regular tools: [RE tools](src/regular.py)
- SSH client: [SSH client](src/ssh.py)
- Samba client: [Samba client](src/samba.py)
- PySide6 tools: [PySide6 tools](src/qt6.py)
- AES tools: [AES tools](src/aes.py)

## Run Tests

### just run tests

```shell
pytest ./tests
```

### run tests with coverage

```shell
coverage run -m pytest ./tests
```

### show coverage report in command line

```shell
coverage report
```

### show coverage report in web page

```shell
coverage html
```

## References

- [pytest: helps you write better programs — pytest documentation](https://docs.pytest.org/en/7.1.x/)
- [Coverage.py — Coverage.py 5.5 documentation](https://coverage.readthedocs.io/en/coverage-5.5/index.html)
- [Welcome to PyCryptodome’s documentation — PyCryptodome 3.14.1 documentation](https://pycryptodome.readthedocs.io/en/latest/index.html)