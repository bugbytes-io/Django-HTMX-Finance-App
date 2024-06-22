from datetime import datetime, timedelta
import pytest
from django.urls import reverse
from tracker.models import Category, Transaction
from pytest_django.asserts import assertTemplateUsed

@pytest.mark.django_db
def test_total_values_appear_on_list_page(user_transactions, client):
    user = user_transactions[0].user
    client.force_login(user)

    income_total = sum(t.amount for t in user_transactions if t.type == 'income')
    expense_total = sum(t.amount for t in user_transactions if t.type == 'expense')
    net = income_total - expense_total

    response = client.get(reverse('transactions-list'))
    assert response.context['total_income'] == income_total
    assert response.context['total_expenses'] == expense_total
    assert response.context['net_income'] == net


@pytest.mark.django_db
def test_transaction_type_filter(user_transactions, client):
    user = user_transactions[0].user
    client.force_login(user)

    # income check
    GET_params = {'transaction_type': 'income'}
    response = client.get(reverse('transactions-list'), GET_params)

    qs = response.context['filter'].qs

    for transaction in qs:
        assert transaction.type == 'income'

    # expense check
    GET_params = {'transaction_type': 'expense'}
    response = client.get(reverse('transactions-list'), GET_params)

    qs = response.context['filter'].qs

    for transaction in qs:
        assert transaction.type == 'expense'


@pytest.mark.django_db
def test_start_end_date_filter(user_transactions, client):
    user = user_transactions[0].user
    client.force_login(user)

    start_date_cutoff = datetime.now().date() - timedelta(days=120)
    GET_params = {'start_date': start_date_cutoff}
    response = client.get(reverse('transactions-list'), GET_params)

    qs = response.context['filter'].qs

    for transaction in qs:
        assert transaction.date >= start_date_cutoff

    end_date_cutoff = datetime.now().date() - timedelta(days=20)
    GET_params = {'end_date': end_date_cutoff}
    response = client.get(reverse('transactions-list'), GET_params)

    qs = response.context['filter'].qs

    for transaction in qs:
        assert transaction.date <= end_date_cutoff

@pytest.mark.django_db
def test_category_filter(user_transactions, client):
    user = user_transactions[0].user
    client.force_login(user)

    # get first two categories' PKs
    category_pks = Category.objects.all()[:2].values_list('pk', flat=True)
    GET_params = {'category': category_pks}

    response = client.get(reverse('transactions-list'), GET_params)

    qs = response.context['filter'].qs

    for transaction in qs:
        assert transaction.category.pk in category_pks


@pytest.mark.django_db
def test_add_transaction_request(user, transaction_dict_params, client):
    client.force_login(user)
    user_transaction_count = Transaction.objects.filter(user=user).count()

    # send request with transaction data
    headers = {'HTTP_HX-Request': 'true'}
    response = client.post(
        reverse('create-transaction'),
        transaction_dict_params,
        **headers
    )

    # assert the count has increased after the POST request
    assert Transaction.objects.filter(user=user).count() == user_transaction_count + 1

    assertTemplateUsed(response, 'tracker/partials/transaction-success.html')


@pytest.mark.django_db
def test_cannot_add_transaction_with_negative_amount(
    user,
    transaction_dict_params,
    client
):
    client.force_login(user)
    user_transaction_count = Transaction.objects.filter(user=user).count()

    transaction_dict_params['amount'] = -44
    response = client.post(
        reverse('create-transaction'),
        transaction_dict_params,
    )

    assert Transaction.objects.filter(user=user).count() == user_transaction_count

    assertTemplateUsed(response, 'tracker/partials/create-transaction.html')
    assert 'HX-Retarget' in response.headers
