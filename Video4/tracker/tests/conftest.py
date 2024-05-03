import pytest 
from tracker.factories import TransactionFactory


@pytest.fixture
def transactions():
    return TransactionFactory.create_batch(20)