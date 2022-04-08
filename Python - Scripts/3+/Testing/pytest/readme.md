the information was obtained from https://docs.pytest.org/, all the credits for the original
authors. 

+ "Pytest will run all files of the form test_*.py or *_test.py in the current directory and its subdirectories" https://docs.pytest.org/en/7.1.x/explanation/goodpractices.html#test-discovery
+ We can run a specific python script using -q, such as pytest -q test_class.py
+ Run tests in a directory `pytest testing/`
+ Run tests with keyword expressions `pytest -k "MyClass and not method"`
+ run tests by node ids `pytest test_mod.py::TestClass::test_method`
+ run tests by marker expressions, for example by slow decorator `pytest -m slow`
+ run tests from packages `pytest --pyargs pkg.testing`

Group of test in classes can bring you:
+ organization
+ sharing fixtures

## Marking test functions with attributes

Using `pytest.mark` helper we can set metadata in the test functions. The full markers are
https://docs.pytest.org/en/7.1.x/reference/reference.html#marks-ref our we can list them by `pytest --markers`

We can register marks in the `pytest.ini` file like this:

```
[pytest]
markers = 
	slow: marks test as slow (deselect with '-m "not slow"')
	serial
```
or we can reflect in `pyproject.tml` file like this:
```
[tool.pytest.ini_options]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "serial",
]
```
Another option is registering the markers in a `pytest_configure`
```
def pytest_configure(config):
    config.addinivalue_line(
        "markers", "env(name): mark test to run only on named environment"
    )
```