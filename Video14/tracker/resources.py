from import_export import resources, fields
from tracker.models import Transaction, Category
from import_export.widgets import ForeignKeyWidget

class TransactionResource(resources.ModelResource):
    category = fields.Field(
        column_name='category',
        attribute='category',
        widget=ForeignKeyWidget(Category, field='name')
    )

    def after_init_instance(self, instance, new, row, **kwargs):
        instance.user = kwargs.get('user')

    class Meta:
        model = Transaction
        fields = (
            'amount',
            'type',
            'date',
            'category',            
        )
        import_id_fields = (
            'amount',
            'type',
            'date',
            'category',              
        )