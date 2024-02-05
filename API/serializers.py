from rest_framework import serializers
from .models import Expense, Budget, User
from django.db.models import Sum
from expTracker import settings
from django.contrib.auth.hashers import make_password

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            user = self.user
            if user and user.check_password(password):
                data['user_id'] = user.id
                data['username'] = user.username
                # Add any other information you want to include in the token payload
            else:
                raise serializers.ValidationError("Invalid credentials")

        return data


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, min_length=settings.MIN_PASSWORD_LENGTH)
    confirm_password = serializers.CharField(
        write_only=True, min_length=settings.MIN_PASSWORD_LENGTH)

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        validated_data['password'] = make_password(password)

        user = User(**validated_data)
        user.is_active = True
        user.save()

        return user


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ("__all__")
        extra_kwargs = {'user': {'read_only': True}}


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ("__all__")
        extra_kwargs = {'user': {'read_only': True}}


class TotalExpensesSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()

    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if start_date and end_date:
            if start_date > end_date:
                raise serializers.ValidationError(
                    "Start date should be earlier than end date.")

        total_expenses = Expense.objects.filter(
            date__range=[start_date, end_date]).aggregate(total_expenses=Sum('amount'))

        return {'total_expenses': total_expenses['total_expenses'] or 0}


class RemainingBudgetSerializer(serializers.Serializer):
    category = serializers.CharField()

    def validate_category(self, value):
        # Check if the category exists in the Budget model
        if not Budget.objects.filter(category=value).exists():
            raise serializers.ValidationError(
                f'Category "{value}" does not exist in the system.')

        return value
