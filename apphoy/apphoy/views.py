from django.shortcuts import redirect


def redirect_view(request):
    """
    Function used as a view that always redirects from an empty url ('') to the persons dashboard.
    """
    response = redirect('/persons/')
    return response
