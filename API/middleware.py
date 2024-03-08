from django.http import HttpResponseForbidden
from .models import Expense, Budget


class UserAssociationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        print(request.path)
        # Check if the request is for an expense or budget endpoint
        if request.path.startswith('/api/expenses/') or request.path.startswith('/api/budgets/'):
            # Ensure the user associated with the object matches the authenticated user
            if hasattr(request, 'user') and request.user.is_authenticated:
                print(request.user.pk)
                if 'pk' in request.resolver_match.kwargs:
                    # If accessing object via pk (e.g., /api/expenses/<pk>/)
                    object_pk = request.resolver_match.kwargs['pk']
                    if request.path.startswith('/api/expenses/'):
                        object_instance = Expense.objects.get(pk=object_pk)
                    elif request.path.startswith('/api/budgets/'):
                        object_instance = Budget.objects.get(pk=object_pk)

                    if object_instance.user != request.user:
                        return HttpResponseForbidden("You are not allowed to perform this action.")

                elif hasattr(request, 'data') and 'user' in request.data:
                    if request.data['user'] != request.user.id:
                        return HttpResponseForbidden("You are not allowed to perform this action.")

        return response
