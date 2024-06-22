from django.db import models 


class TransactionQuerySet(models.QuerySet):
    def get_expenses(self):
        return self.filter(type='expense')
    
    def get_income(self):
        return self.filter(type='income')
    
    def get_total_expenses(self):
        return self.get_expenses().aggregate(
            total=models.Sum('amount')
        )['total'] or 0

    def get_total_income(self):
        return self.get_income().aggregate(
            total=models.Sum('amount')
        )['total'] or 0