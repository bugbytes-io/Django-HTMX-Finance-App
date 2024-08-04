from import_export import resources, fields
from tracker.models import Transaction, Category
from import_export.widgets import ForeignKeyWidget

class TransactionResource(resources.ModelResource):
    category = fields.Field(
        column_name='category',
        attribute='category',
        widget=ForeignKeyWidget(Category, field='name')
    )

    class Meta:
        model = Transaction
        fields = (
            'amount',
            'type',
            'date',
            'category',            
        )