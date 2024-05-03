from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from tracker.models import Transaction
from tracker.filters import TransactionFilter


# Create your views here.
def index(request):
    return render(request, 'tracker/index.html')


@login_required
def transactions_list(request):
    transaction_filter = TransactionFilter(
        request.GET,
        queryset=Transaction.objects.filter(user=request.user).select_related('category')
    )
    context = {'filter': transaction_filter}

    if request.htmx:
        return render(request, 'tracker/partials/transactions-container.html', context)

    return render(request, 'tracker/transactions-list.html', context)