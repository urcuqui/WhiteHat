# assert that a certain exception is raised 
# uses the raises helper to assert that some code raises an exception

import pytest

def f():
    raise SystemExit(1)

def test_mytest():
    with pytest.raises(SystemExit):
        f()
