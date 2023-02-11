import functools
from django.shortcuts import redirect


def is_authenticated(view_fn, redirect_url="index"):
    @functools.wraps(view_fn)
    def wrapper(request, *args, **kwargs):

        if request.user.is_authenticated:
            return view_fn(request, *args, **kwargs)

        return redirect(redirect_url)

    return wrapper
