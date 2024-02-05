from django.urls import path
from .views import (
    CategoryWiseExpensesAPIView, ExpenseListCreateView, ExpenseRetrieveUpdateDestroyView,
    BudgetListCreateView, BudgetRetrieveUpdateDestroyView, RemainingBudgetAPIView, UserRegistrationAPIView, TotalExpensesAPIView
)

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('expenses/', ExpenseListCreateView.as_view(), name='expense-list-create'),
    path('expenses/<int:pk>/', ExpenseRetrieveUpdateDestroyView.as_view(),
         name='expense-retrieve-update-destroy'),
    path('budgets/', BudgetListCreateView.as_view(), name='budget-list-create'),
    path('budgets/<int:pk>/', BudgetRetrieveUpdateDestroyView.as_view(),
         name='budget-retrieve-update-destroy'),
    path('total-expenses/', TotalExpensesAPIView.as_view(), name='total-expenses'),
    path('category-wise-expenses/', CategoryWiseExpensesAPIView.as_view(),
         name='category-wise-expenses'),
    path('remaining-budget/', RemainingBudgetAPIView.as_view(),
         name='remaining-budget'),
]
