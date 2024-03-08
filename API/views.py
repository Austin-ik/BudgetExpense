from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, AllowAny
from API.mixins import UserOwnedQuerysetMixin
from API.models import Budget, Expense, User
from .serializers import BudgetSerializer, CustomTokenObtainPairSerializer, ExpenseSerializer, RemainingBudgetSerializer, TotalExpensesSerializer, UserSerializer
from rest_framework.response import Response
from django.core.exceptions import PermissionDenied
from rest_framework import status, generics
from rest_framework.serializers import ValidationError
from django.db.models import Sum


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserRegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(is_active=False)
        user.save()
        print(user.id)

        response_data = {
            "user_id": user.id,
            "message": "Your account was created successfully"
        }
        return Response(response_data, status=status.HTTP_201_CREATED)


class ExpenseListCreateView(UserOwnedQuerysetMixin, generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer
    model = Expense
    queryset = Expense.objects.all()

    # def get_queryset(self):
    #     return Expense.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

        data = serializer.data
        return Response(data, status=status.HTTP_201_CREATED)


class ExpenseRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()

    # def get_queryset(self):
    #     return Expense.objects.filter(user=self.request.user)


class BudgetListCreateView(UserOwnedQuerysetMixin, generics.ListCreateAPIView):
    serializer_class = BudgetSerializer
    model = Budget
    queryset = Budget.objects.all()


    # def get_queryset(self):
    #     return Budget.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        category = serializer.validated_data.get('category')

        # Check if a budget already exists for the specified category and user
        existing_budget = Budget.objects.filter(
            user=self.request.user, category=category).first()

        if existing_budget:
            # If a budget already exists, return a response indicating to update it
            message = f'A budget already exists for category "{category}". Update it instead of creating a new one.'
            return Response({'detail': message}, status=status.HTTP_400_BAD_REQUEST)

        # If no budget exists, proceed with creating a new one
        serializer.save(user=self.request.user)
        data = serializer.data
        return Response(data, status=status.HTTP_201_CREATED)


class BudgetRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BudgetSerializer
    queryset = Budget.objects.all()

    # def get_queryset(self):
    #     return Budget.objects.filter(user=self.request.user)


class TotalExpensesAPIView(generics.GenericAPIView):
    serializer_class = TotalExpensesSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryWiseExpensesAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = self.request.user

        # Retrieve all unique expense categories for the authenticated user
        categories = Expense.objects.filter(user=user).values_list(
            'category', flat=True).distinct()

        category_wise_expenses = []

        # Calculate total expenses for each category
        for category in categories:
            total_expenses = Expense.objects.filter(user=user, category=category).aggregate(
                total_expenses=Sum('amount'))['total_expenses']
            total_expenses = total_expenses or 0

            category_wise_expenses.append({
                'category': category,
                'total_expenses': total_expenses
            })

        return Response(category_wise_expenses, status=status.HTTP_201_CREATED)


class RemainingBudgetAPIView(generics.CreateAPIView):
    serializer_class = RemainingBudgetSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        category_name = serializer.validated_data['category']
        message = None

        # Get the total budget for the category for the authenticated user
        try:
            budget = Budget.objects.get(
                user=request.user, category=category_name)
            total_budget = budget.amount
        except Budget.DoesNotExist:
            return Response({'detail': f'No budget found for category "{category_name}"'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the total expenses for the category for the authenticated user
        total_expenses = Expense.objects.filter(user=request.user, category=category_name).aggregate(
            total_expenses=Sum('amount'))['total_expenses'] or 0

        # Calculate the remaining budget
        remaining_budget = total_budget - total_expenses
        if remaining_budget < 0:
            message = f"You have spent beyond your budget for {category_name} by {abs(remaining_budget)}"

        response_data = {
            'category': category_name,
            'remaining_budget': remaining_budget,
            'Message': message
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
