import pytest

@pytest.fixture
def none_security(config):
    from pymco.security import none
    return none.NoneProvider(config)
