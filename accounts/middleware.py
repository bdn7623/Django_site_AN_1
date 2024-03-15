from django.shortcuts import redirect
from django.urls import reverse


class ProfileCompletionMiddleware:
    """
    Middleware to ensure users complete their profile.

    This middleware checks if a user is authenticated and has a profile.
    If the user is authenticated but doesn't have a profile, it redirects
    them to create a profile.

    Attributes:
    - get_response: The next middleware in the chain or the view.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        Check if user is authenticated and has a profile.
        If not, redirect them to create a profile.

        Parameters:
        - request: The HTTP request.

        Returns:
        - response: The HTTP response.
        """
        if request.user.is_authenticated and not hasattr(request.user, 'profile'):
            create_profile_url = reverse('accounts:profile_create')
            if request.path != create_profile_url:
                return redirect(create_profile_url)

        response = self.get_response(request)
        return response
