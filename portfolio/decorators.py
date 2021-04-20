from functools import wraps
from django.shortcuts import redirect

from portfolio.models import Testimonial


def check_if_testimonial_is_answered(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        testimonial = Testimonial.objects.get(hash_key=kwargs['hash_key'])
        if testimonial.is_answered is False:
            return function(request, *args, **kwargs)

        return redirect('homepage')

    return wrap

