import pytest
"""
The tmp_path_factory is a session-scoped fixture which can be used to create arbitrary temporary directories from any other fixture or test.

For example, suppose your test suite needs a large image on disk, which is generated procedurally. Instead of computing the same image for each test that uses it into its own tmp_path, you can generate it once per-session to save time:

https://docs.pytest.org/en/7.1.x/reference/reference.html#tmp-path-factory-factory-api
"""
@pytest.fixture(scope="session")
def image_file(tmp_path_factory):
    img = compute_expensive_image()
    fn = tmp_path_factory.mktemp("data") / "img.png"
    
# contents of test_image.py
def test_histogram():
    img = load_image(image_file)
    