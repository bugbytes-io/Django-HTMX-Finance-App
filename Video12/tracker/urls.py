from django.urls import path
from tracker import views


urlpatterns = [
    path("", views.index, name='index'),
    path("transactions/", views.transactions_list, name='transactions-list'),
    path('transactions/create/', views.create_transaction, name='create-transaction'),

    path('transactions/<int:pk>/update/', views.update_transaction, name='update-transaction'),
    path('transactions/<int:pk>/delete/', views.delete_transaction, name='delete-transaction'),

    path('get-transactions/', views.get_transactions, name='get-transactions'),

    path('transactions/charts', views.transaction_charts, name='transactions-charts'),
]
