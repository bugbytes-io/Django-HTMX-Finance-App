import pytest 
from tracker.factories import TransactionFactory, UserFactory


@pytest.fixture
def transactions():
    return TransactionFactory.create_batch(20)

@pytest.fixture
def user_transactions():
    user = UserFactory()
    return TransactionFactory.create_batch(20, user=user)