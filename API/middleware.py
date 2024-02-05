# api/middleware.py
from django.http import HttpResponseForbidden

class UserAssociationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request is for an expense or budget endpoint
        if request.path.startswith('/api/expenses/') or request.path.startswith('/api/budgets/'):
            # Ensure the user associated with the object matches the authenticated user
            if hasattr(request, 'user') and request.user.is_authenticated:
                # Assuming your Expense and Budget models have a 'user' field
                if hasattr(request, 'data') and 'user' in request.data:
                    if request.data['user'] != request.user.id:
                        return HttpResponseForbidden("You are not allowed to perform this action.")
                elif hasattr(request, 'obj') and request.obj.user != request.user:
                    return HttpResponseForbidden("You are not allowed to perform this action.")

        response = self.get_response(request)
        return response
