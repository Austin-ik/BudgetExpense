from django.contrib import admin

from .models import Expense, Budget


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'category', 'description', 'date')
    search_fields = ('category',)
    
    
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'amount')
    search_fields = ('category',)
    
    


# Register your models here.
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Budget, BudgetAdmin)